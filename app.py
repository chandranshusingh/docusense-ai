"""
Docusense OCR Prototype - Flask Backend Application

A comprehensive, local-first OCR service for processing multiple file formats.
This prototype provides web interface, advanced OCR settings, and REST API endpoints
for document upload and processing with structured data extraction capabilities.
"""
# pylint: disable=too-many-lines

import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import config

# Initialize global variables first
PDF_TEXT_EXTRACTION_AVAILABLE = False
OCR_AVAILABLE = False

# Try to import OCR libraries with graceful fallback
try:
    import pytesseract
    from PIL import Image, ImageEnhance
    import pdf2image
    from docx import Document
    import pandas as pd

    # For enhanced PDF processing
    try:
        import PyPDF2
        PDF_TEXT_EXTRACTION_AVAILABLE = True
    except ImportError:
        PDF_TEXT_EXTRACTION_AVAILABLE = False

    # Configure Tesseract OCR path - try multiple locations
    TESSERACT_FOUND = False

    for tesseract_path in config.TESSERACT_PATHS:
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            # Test if Tesseract is working
            pytesseract.get_tesseract_version()
            TESSERACT_FOUND = True
            print(f"✅ Tesseract found at: {tesseract_path}")
            break
        except (pytesseract.TesseractNotFoundError, FileNotFoundError, OSError):
            continue

    # Fallback: try to force set the most common Windows path
    if not TESSERACT_FOUND:
        FORCE_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(FORCE_PATH):
            pytesseract.pytesseract.tesseract_cmd = FORCE_PATH
            try:
                pytesseract.get_tesseract_version()
                TESSERACT_FOUND = True
                print(f"✅ Tesseract found at: {FORCE_PATH}")
            except (pytesseract.TesseractNotFoundError, OSError):
                pass

    OCR_AVAILABLE = TESSERACT_FOUND
except ImportError:
    OCR_AVAILABLE = False

# Initialize Flask application
app = Flask(__name__)

# Configure application settings from config file
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
if not os.path.exists(config.UPLOAD_FOLDER):
    os.makedirs(config.UPLOAD_FOLDER)


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension

    Args:
        filename (str): The name of the uploaded file

    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS)


def get_available_languages():
    """
    Detect available Tesseract language packs

    Returns:
        list: List of available language codes
    """
    if not OCR_AVAILABLE:
        return ['eng']  # Default to English only in demo mode

    try:
        # Get available languages from Tesseract
        # Note: get_languages() doesn't take a config parameter in the same way
        available_langs = pytesseract.get_languages()

        # Filter to only include languages we have configured
        supported_langs = []
        for lang_code in available_langs:
            if lang_code in config.AVAILABLE_LANGUAGES:
                supported_langs.append(lang_code)

        # Always include English as fallback
        if 'eng' not in supported_langs:
            supported_langs.insert(0, 'eng')

        return supported_langs
    except (pytesseract.TesseractNotFoundError, RuntimeError):
        return ['eng']  # Fallback to English only


def get_tesseract_config(engine_mode, psm_mode, language='eng'):
    """
    Generate Tesseract configuration string based on parameters

    Args:
        engine_mode (str): OCR engine mode key
        psm_mode (str): Page segmentation mode key
        language (str): Language code

    Returns:
        tuple: (language, config_string)
    """
    # Get numeric values from config mappings
    oem = config.OCR_ENGINE_MODES.get(engine_mode, config.OCR_ENGINE_MODES['lstm'])
    psm = config.PAGE_SEGMENTATION_MODES.get(psm_mode, config.PAGE_SEGMENTATION_MODES['auto'])

    # Validate language availability
    available_languages = get_available_languages()
    if language not in available_languages:
        language = 'eng'  # Fallback to English

    # Build configuration string
    config_string = f'--oem {oem} --psm {psm}'

    return language, config_string


def enhance_image_for_ocr(image):
    """
    Enhanced image preprocessing for better OCR on ID cards and documents

    Args:
        image (PIL.Image): The input image

    Returns:
        PIL.Image: Enhanced image for OCR
    """
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Apply slight sharpening to improve text clarity
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.2)  # Slight sharpening

    # Enhance contrast for better text/background separation
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.1)  # Slight contrast boost

    # Apply slight brightness adjustment if image is too dark
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.05)  # Very slight brightness boost

    return image


def preprocess_image_for_dpi(image, dpi_setting):
    """
    Preprocess image based on DPI setting for better OCR accuracy

    Args:
        image (PIL.Image): The input image
        dpi_setting (str): DPI setting key ('low', 'medium', 'high')

    Returns:
        PIL.Image: Processed image
    """
    target_dpi = config.DPI_PRESETS.get(dpi_setting, config.DPI_PRESETS['medium'])

    # Get original DPI or assume 72 if not available
    original_dpi = image.info.get('dpi', (72, 72))
    if isinstance(original_dpi, (int, float)):
        original_dpi = (original_dpi, original_dpi)

    # First enhance the image quality for better OCR
    enhanced_image = enhance_image_for_ocr(image)

    # Calculate scaling factor - be more conservative with ID cards
    scale_factor = target_dpi / original_dpi[0]

    # Limit scaling to prevent over-processing of ID cards
    scale_factor = min(scale_factor, 2.0)  # Max 2x scaling
    scale_factor = max(scale_factor, 0.8)  # Min 0.8x scaling

    # Only resize if scale factor is significantly different (higher threshold for ID cards)
    if abs(scale_factor - 1.0) > 0.15:
        new_width = int(enhanced_image.width * scale_factor)
        new_height = int(enhanced_image.height * scale_factor)

        # Use high-quality resampling with compatibility handling
        try:
            # Try new Resampling enum (Pillow 10.0+)
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            # Fallback for older Pillow versions
            resample_method = getattr(Image, 'LANCZOS', 1)  # 1 is the numeric value for LANCZOS

        enhanced_image = enhanced_image.resize((new_width, new_height), resample_method)

    return enhanced_image


def calculate_dpi_scaling_factors(original_image, processed_image):
    """
    Calculate scaling factors between original and processed images

    Args:
        original_image (PIL.Image): Original image
        processed_image (PIL.Image): Processed image after DPI adjustment

    Returns:
        tuple: (dpi_scale_x, dpi_scale_y) scaling factors
    """
    original_width, original_height = original_image.size
    processed_width, processed_height = processed_image.size
    dpi_scale_x = processed_width / original_width
    dpi_scale_y = processed_height / original_height
    return dpi_scale_x, dpi_scale_y


def clean_and_scale_ocr_data(ocr_data, dpi_scale_x, dpi_scale_y):
    """
    Clean OCR data and scale coordinates back to original image dimensions

    Args:
        ocr_data (dict): Raw OCR data from Tesseract
        dpi_scale_x (float): X-axis scaling factor
        dpi_scale_y (float): Y-axis scaling factor

    Returns:
        list: Cleaned and scaled OCR data entries
    """
    cleaned_data = []
    for i in range(len(ocr_data['text'])):
        text = ocr_data['text'][i].strip()
        if text:  # Only include entries with actual text content
            # Scale coordinates back to original image dimensions
            scaled_left = int(ocr_data['left'][i] / dpi_scale_x)
            scaled_top = int(ocr_data['top'][i] / dpi_scale_y)
            scaled_width = int(ocr_data['width'][i] / dpi_scale_x)
            scaled_height = int(ocr_data['height'][i] / dpi_scale_y)

            cleaned_data.append({
                'text': text,
                'confidence': int(ocr_data['conf'][i]),
                'left': scaled_left,
                'top': scaled_top,
                'width': scaled_width,
                'height': scaled_height
            })
    return cleaned_data


def build_ocr_result(cleaned_data, dpi_setting, language, engine_mode, psm_mode):
    """
    Build the final OCR result with metadata

    Args:
        cleaned_data (list): Cleaned OCR data entries
        dpi_setting (str): DPI setting used
        language (str): Language code used
        engine_mode (str): OCR engine mode used
        psm_mode (str): Page segmentation mode used

    Returns:
        dict: Complete OCR result with data and settings
    """
    return {
        'data': cleaned_data,
        'ocr_settings': {
            'dpi_setting': dpi_setting,
            'dpi_value': config.DPI_PRESETS.get(dpi_setting, 300),
            'language': language,
            'language_name': config.AVAILABLE_LANGUAGES.get(language, language),
            'engine_mode': engine_mode,
            'psm_mode': psm_mode
        }
    }


def process_image(filepath, dpi_setting='medium', language='eng',
                  engine_mode='lstm', psm_mode='auto'):
    """
    Process an image file using OCR to extract text with bounding boxes

    Args:
        filepath (str): Path to the image file
        dpi_setting (str): DPI setting for image preprocessing
        language (str): Language code for OCR
        engine_mode (str): OCR engine mode
        psm_mode (str): Page segmentation mode

    Returns:
        dict: OCR data with text and bounding box information plus processing metadata
    """
    if not OCR_AVAILABLE:
        return {'data': [{'text': 'OCR libraries not available - demo mode',
                         'confidence': 0, 'left': 0, 'top': 0, 'width': 100, 'height': 20}]}
    try:
        # Open and preprocess image
        image = Image.open(filepath)
        processed_image = preprocess_image_for_dpi(image, dpi_setting)

        # Calculate scaling factors for coordinate correction
        dpi_scale_x, dpi_scale_y = calculate_dpi_scaling_factors(image, processed_image)

        # Get Tesseract configuration
        lang, config_string = get_tesseract_config(engine_mode, psm_mode, language)

        # Run Tesseract OCR with advanced settings
        ocr_data = pytesseract.image_to_data(
            processed_image,
            lang=lang,
            config=config_string,
            output_type=pytesseract.Output.DICT
        )

        # Clean up OCR data and scale coordinates back to original image size
        cleaned_data = clean_and_scale_ocr_data(ocr_data, dpi_scale_x, dpi_scale_y)

        # Build and return final result
        return build_ocr_result(cleaned_data, dpi_setting, lang, engine_mode, psm_mode)

    except pytesseract.TesseractNotFoundError as e:
        raise ValueError(f"Tesseract not found: {str(e)}") from e
    except pytesseract.TesseractError as e:
        raise ValueError(f"OCR processing failed: {str(e)}") from e
    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"Image processing failed: {str(e)}") from e


def extract_text_from_pdf(filepath):
    """
    Extract text directly from text-based PDF using PyPDF2

    Args:
        filepath (str): Path to the PDF file

    Returns:
        tuple: (success: bool, text: str, page_count: int)
    """
    if not PDF_TEXT_EXTRACTION_AVAILABLE:
        return False, "", 0

    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                return False, "PDF is password-protected", len(pdf_reader.pages)

            text_content = []
            page_count = len(pdf_reader.pages)

            # Extract text from each page
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text().strip()
                if page_text:  # Only include pages with text
                    text_content.append(f"--- Page {page_num} ---\n{page_text}")

            full_text = '\n\n'.join(text_content)
            return len(full_text.strip()) > 0, full_text, page_count

    except (OSError, UnicodeDecodeError, RuntimeError):
        return False, "", 0


def process_pdf(filepath, dpi_setting='medium', language='eng',
                 engine_mode='lstm', psm_mode='auto'):
    """
    Enhanced PDF processing with multi-page support and text extraction

    Args:
        filepath (str): Path to the PDF file
        dpi_setting (str): DPI setting for image preprocessing
        language (str): Language code for OCR
        engine_mode (str): OCR engine mode
        psm_mode (str): Page segmentation mode

    Returns:
        dict: OCR data with page information and processing metadata
    """
    if not OCR_AVAILABLE:
        return {'data': [{'text': 'PDF processing not available - demo mode',
                         'confidence': 0, 'left': 0, 'top': 0, 'width': 200, 'height': 20}]}

    try:
        # First attempt: Try direct text extraction for text-based PDFs
        if config.PDF_TEXT_EXTRACTION_FIRST:
            text_success, extracted_text, page_count = extract_text_from_pdf(filepath)

            if text_success and extracted_text.strip():
                return {
                    'data': {'text_only': extracted_text},
                    'processing_method': 'text_extraction',
                    'page_count': page_count,
                    'message': f'Text extracted from {page_count} page(s)'
                }

        # Second attempt: OCR processing for image-based PDFs
        return process_pdf_with_ocr(filepath, dpi_setting, language, engine_mode, psm_mode)

    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"PDF processing failed: {str(e)}") from e


def convert_pdf_to_images(filepath, dpi_setting):
    """
    Convert PDF pages to images for OCR processing

    Args:
        filepath (str): Path to the PDF file
        dpi_setting (str): DPI setting for conversion

    Returns:
        list: List of PIL Image objects
    """
    pdf_dpi = config.DPI_PRESETS.get(dpi_setting, config.DPI_PRESETS['medium'])
    max_pages = config.MAX_PDF_PAGES if config.MAX_PDF_PAGES > 0 else None

    return pdf2image.convert_from_path(
        filepath,
        dpi=pdf_dpi,
        last_page=max_pages,
        poppler_path=config.POPPLER_PATH
    )


def process_pdf_page_with_ocr(image, page_num, base_filename, ocr_settings):
    """
    Process a single PDF page with OCR

    Args:
        image: PIL Image object
        page_num (int): Page number
        base_filename (str): Base filename for saving
        ocr_settings (dict): OCR processing settings

    Returns:
        tuple: (page_ocr_result, image_filename)
    """
    # Save the converted image
    image_filename = f"{base_filename}_page_{page_num}.png"
    image_path = os.path.join(config.UPLOAD_FOLDER, image_filename)
    image.save(image_path, 'PNG')

    # Process the page with OCR
    page_ocr_result = process_image(image_path, **ocr_settings)

    # Add page information to each OCR entry
    for entry in page_ocr_result['data']:
        entry['page'] = page_num

    return page_ocr_result, image_filename


def build_pdf_ocr_result(images, filepath, ocr_settings):
    """
    Process PDF images and build OCR result

    Args:
        images: List of PIL images
        filepath: Original PDF file path
        ocr_settings: Dictionary of OCR settings

    Returns:
        dict: Complete OCR result
    """
    base_filename = os.path.splitext(os.path.basename(filepath))[0]
    page_results = [
        process_pdf_page_with_ocr(image, page_num, base_filename, ocr_settings)
        for page_num, image in enumerate(images, 1)
    ]

    # Extract data and filenames
    all_data = [item for page_result, _ in page_results for item in page_result['data']]
    all_images = [filename for _, filename in page_results]
    first_settings = next(
        (pr['ocr_settings'] for pr, _ in page_results if 'ocr_settings' in pr), None
    )

    result = {
        'data': all_data,
        'converted_images': all_images,
        'processing_method': 'ocr',
        'page_count': len(images),
        'message': f'OCR processed {len(images)} page(s)'
    }

    if first_settings:
        result['ocr_settings'] = first_settings

    return result


def process_pdf_with_ocr(filepath, dpi_setting='medium', language='eng',
                         engine_mode='lstm', psm_mode='auto'):
    """
    Process PDF using OCR with multi-page support and advanced settings

    Args:
        filepath (str): Path to the PDF file
        dpi_setting (str): DPI setting for image preprocessing
        language (str): Language code for OCR
        engine_mode (str): OCR engine mode
        psm_mode (str): Page segmentation mode

    Returns:
        dict: OCR data with page information and processing metadata
    """
    try:
        # Convert PDF pages to images
        images = convert_pdf_to_images(filepath, dpi_setting)
        if not images:
            raise ValueError("No pages found in PDF")

        # Process pages and build result
        ocr_settings = {
            'dpi_setting': dpi_setting, 'language': language,
            'engine_mode': engine_mode, 'psm_mode': psm_mode
        }
        return build_pdf_ocr_result(images, filepath, ocr_settings)

    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"PDF OCR processing failed: {str(e)}") from e


def process_docx(filepath):
    """
    Extract text content from DOCX file

    Args:
        filepath (str): Path to the DOCX file

    Returns:
        dict: Extracted text content
    """
    if not OCR_AVAILABLE:
        return {'data': {'text_only': 'DOCX processing not available - demo mode'}}
    try:
        # Open and read DOCX document
        doc = Document(filepath)

        # Extract text from all paragraphs
        text_content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only include non-empty paragraphs
                text_content.append(paragraph.text.strip())

        # Join all paragraphs with newlines
        full_text = '\n'.join(text_content)

        return {'data': {'text_only': full_text}}

    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"DOCX processing failed: {str(e)}") from e


def process_txt(filepath):
    """
    Read and return content from plain text file

    Args:
        filepath (str): Path to the TXT file

    Returns:
        dict: File content as text
    """
    try:
        # Read text file content with proper encoding handling
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read().strip()

        return {'data': {'text_only': content}}

    except FileNotFoundError as e:
        raise ValueError(f"Text file not found: {str(e)}") from e
    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"Text file processing failed: {str(e)}") from e


def process_csv(filepath):
    """
    Process CSV file and extract structured content

    Args:
        filepath (str): Path to the CSV file

    Returns:
        dict: Structured CSV data as text with table formatting
    """
    try:
        # Read CSV file with pandas for robust handling
        df = pd.read_csv(
            filepath,
            encoding=config.CSV_ENCODING,
            delimiter=config.CSV_DELIMITER,
            on_bad_lines='skip',  # Skip problematic lines
            dtype=str,  # Read all as strings to preserve formatting
            keep_default_na=False  # Don't convert empty strings to NaN
        )

        # Limit the data size to avoid memory issues
        if len(df) > config.EXCEL_MAX_ROWS:
            df = df.head(config.EXCEL_MAX_ROWS)
            truncated_message = f" (truncated to {config.EXCEL_MAX_ROWS} rows)"
        else:
            truncated_message = ""

        if len(df.columns) > config.EXCEL_MAX_COLUMNS:
            df = df.iloc[:, :config.EXCEL_MAX_COLUMNS]
            truncated_message += f" (truncated to {config.EXCEL_MAX_COLUMNS} columns)"

        # Convert to formatted string representation
        formatted_content = []
        formatted_content.append(
            f"CSV File Content ({len(df)} rows, {len(df.columns)} columns){truncated_message}"
        )
        formatted_content.append("=" * 50)

        # Add column headers
        header_row = " | ".join(df.columns)
        formatted_content.append(header_row)
        formatted_content.append("-" * len(header_row))

        # Add data rows
        for _, row in df.iterrows():
            row_text = " | ".join(
                str(cell) if pd.notna(cell) and str(cell).strip() else "" for cell in row
            )
            formatted_content.append(row_text)

        full_text = '\n'.join(formatted_content)

        return {
            'data': {'text_only': full_text},
            'file_type': 'csv',
            'rows': len(df),
            'columns': len(df.columns)
        }

    except pd.errors.EmptyDataError:
        return {'data': {'text_only': 'CSV file is empty or contains no data'}}
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing failed: {str(e)}") from e
    except FileNotFoundError as e:
        raise ValueError(f"CSV file not found: {str(e)}") from e
    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"CSV processing failed: {str(e)}") from e


def format_excel_sheet_data(df, sheet_name, sheet_idx, original_size):
    """
    Helper function to format individual Excel sheet data

    Args:
        df (DataFrame): Sheet data
        sheet_name (str): Name of the sheet
        sheet_idx (int): Index of the sheet
        original_size (tuple): Original (rows, cols) before truncation

    Returns:
        list: Formatted content lines for the sheet
    """
    sheet_content = []
    truncated_msg = ""

    if original_size[0] > config.EXCEL_MAX_ROWS:
        truncated_msg = f" (truncated to {config.EXCEL_MAX_ROWS} rows)"
    if original_size[1] > config.EXCEL_MAX_COLUMNS:
        truncated_msg += f" (truncated to {config.EXCEL_MAX_COLUMNS} columns)"

    # Add sheet information
    sheet_content.append(f"\nSheet {sheet_idx + 1}: '{sheet_name}'")
    sheet_content.append(
        f"Original size: {original_size[0]} rows, {original_size[1]} columns{truncated_msg}"
    )
    sheet_content.append("-" * 40)

    if df.empty:
        sheet_content.append("(Sheet is empty)")
        return sheet_content

    # Add headers and data
    header_row = " | ".join(df.columns)
    sheet_content.append(header_row)
    sheet_content.append("." * min(len(header_row), 80))

    # Add data rows
    for _, row in df.iterrows():
        row_text = " | ".join(
            str(cell) if pd.notna(cell) and str(cell).strip() else ""
            for cell in row
        )
        sheet_content.append(row_text)

    return sheet_content


def process_excel(filepath):
    """
    Process Excel file (.xls, .xlsx) and extract structured content

    Args:
        filepath (str): Path to the Excel file

    Returns:
        dict: Structured Excel data as text with sheet information
    """
    try:
        # Read Excel file and get all sheet names
        excel_file = pd.ExcelFile(filepath)
        sheet_names = excel_file.sheet_names

        formatted_content = []
        formatted_content.append(f"Excel File Content ({len(sheet_names)} sheet(s))")
        formatted_content.append("=" * 60)

        # Process each sheet
        for sheet_idx, sheet_name in enumerate(sheet_names):
            try:
                # Read and limit sheet data
                df = pd.read_excel(
                    excel_file,
                    sheet_name=sheet_name,
                    dtype=str,
                    keep_default_na=False
                )

                original_size = df.shape
                df = df.head(config.EXCEL_MAX_ROWS)
                df = df.iloc[:, :config.EXCEL_MAX_COLUMNS]

                # Format sheet data using helper function
                sheet_content = format_excel_sheet_data(df, sheet_name, sheet_idx, original_size)
                formatted_content.extend(sheet_content)

            except (pd.errors.ParserError, ValueError, KeyError) as sheet_error:
                formatted_content.append(
                    f"Error processing sheet '{sheet_name}': {str(sheet_error)}"
                )

        return {
            'data': {'text_only': '\n'.join(formatted_content)},
            'file_type': 'excel',
            'sheets': len(sheet_names),
            'sheet_names': sheet_names
        }

    except FileNotFoundError as e:
        raise ValueError(f"Excel file not found: {str(e)}") from e
    except (RuntimeError, ValueError, OSError) as e:
        raise ValueError(f"Excel processing failed: {str(e)}") from e


@app.route('/')
def index():
    """
    Root route that serves the main HTML page
    Returns the index.html template for the OCR service interface
    """
    return render_template('index.html')


def validate_upload_request():
    """
    Validate file upload request

    Returns:
        tuple: (file, error_response) - error_response is None if valid
    """
    if 'file' not in request.files:
        return None, ({'error': 'No file provided',
                      'message': 'Please select a file to upload'}, 400)

    file = request.files['file']

    if file.filename == '':
        return None, ({'error': 'No file selected',
                      'message': 'Please select a valid file'}, 400)

    if not allowed_file(file.filename):
        supported_formats = ", ".join(config.ALLOWED_EXTENSIONS).upper()
        return None, ({'error': 'Invalid file type',
                      'message': f'Supported formats: {supported_formats}'}, 400)

    return file, None


def extract_and_validate_ocr_settings():
    """
    Extract and validate OCR settings from form data

    Returns:
        dict: Validated OCR settings
    """
    # Extract settings with defaults
    settings = {
        'dpi_setting': request.form.get('dpi_setting', config.DEFAULT_DPI_SETTING),
        'language': request.form.get('language', config.DEFAULT_LANGUAGE),
        'engine_mode': request.form.get('engine_mode', config.DEFAULT_OCR_ENGINE_MODE),
        'psm_mode': request.form.get('psm_mode', config.DEFAULT_PSM_MODE)
    }

    # Validate settings
    if settings['dpi_setting'] not in config.DPI_PRESETS:
        settings['dpi_setting'] = config.DEFAULT_DPI_SETTING
    if settings['language'] not in config.AVAILABLE_LANGUAGES:
        settings['language'] = config.DEFAULT_LANGUAGE
    if settings['engine_mode'] not in config.OCR_ENGINE_MODES:
        settings['engine_mode'] = config.DEFAULT_OCR_ENGINE_MODE
    if settings['psm_mode'] not in config.PAGE_SEGMENTATION_MODES:
        settings['psm_mode'] = config.DEFAULT_PSM_MODE

    return settings


def process_file_by_type(file_path, file_extension, ocr_settings):
    """
    Process file based on its type

    Args:
        file_path (str): Path to the uploaded file
        file_extension (str): File extension
        ocr_settings (dict): OCR processing settings

    Returns:
        tuple: (result, message) or raises ValueError for unsupported types
    """
    if file_extension in ['png', 'jpg', 'jpeg']:
        return (process_image(file_path, **ocr_settings), 'Image processed successfully')
    if file_extension == 'pdf':
        return (process_pdf(file_path, **ocr_settings), 'PDF processed successfully')
    if file_extension == 'docx':
        return (process_docx(file_path), 'DOCX processed successfully')
    if file_extension == 'txt':
        return (process_txt(file_path), 'TXT processed successfully')
    if file_extension == 'csv':
        return (process_csv(file_path), 'CSV processed successfully')
    if file_extension in ['xls', 'xlsx']:
        return (process_excel(file_path), 'Excel processed successfully')

    raise ValueError(f'File type {file_extension} is not supported')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and processing requests
    Validates uploaded files and initiates OCR processing

    Returns:
        JSON response with success/error status and processing results
    """
    try:
        # Validate request and file data
        file, error_response = validate_upload_request()
        if error_response:
            return jsonify(error_response[0]), error_response[1]

        # Extract and validate OCR settings
        ocr_settings = extract_and_validate_ocr_settings()

        # Generate unique filename to avoid conflicts
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())[:8]  # Short unique ID
        filename = f"{unique_id}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file with unique name
        file.save(file_path)

        # Process file based on type
        result, message = process_file_by_type(file_path, file_extension, ocr_settings)

        # Add metadata to result
        result['filename'] = filename
        result['message'] = message
        return jsonify(result), 200

    except ValueError as e:
        error_message = str(e)
        print(f"❌ ValueError in upload_file: {error_message}")
        if 'not supported' in error_message:
            return jsonify({'error': 'Unsupported file type', 'message': error_message}), 400
        return jsonify({'error': 'Processing failed', 'message': error_message}), 422
    except OSError as e:
        error_message = str(e)
        print(f"❌ OSError in upload_file: {error_message}")
        return jsonify({
            'error': 'File save failed',
            'message': f'Unable to save file: {error_message}'
        }), 500
    except RuntimeError as e:
        # Catch all unexpected errors
        error_message = str(e)
        print(f"❌ Unexpected error in upload_file: {error_message}")
        print(f"Error type: {type(e).__name__}")
        return jsonify({
            'error': 'Internal server error',
            'message': f'Unexpected error: {error_message}'
        }), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded or processed files to the frontend
    This route enables the frontend to access and display processed images

    Args:
        filename (str): The name of the file to serve

    Returns:
        File response for the requested file
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# REST API Endpoints - Version 1
@app.route('/api/v1/ocr', methods=['POST'])
def api_ocr():
    """
    REST API endpoint for OCR processing
    Accepts file uploads and returns structured JSON results

    Returns:
        JSON response with OCR data or error information
    """
    # Validate request and file data (reuse existing validation)
    file, error_response = validate_upload_request()
    if error_response:
        return jsonify(error_response[0]), error_response[1]

    # Extract and validate OCR settings (reuse existing validation)
    ocr_settings = extract_and_validate_ocr_settings()

    try:
        # Generate unique filename to avoid conflicts
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())[:8]  # Short unique ID
        filename = f"{unique_id}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file with unique name
        file.save(file_path)

        # Process file and return results
        result, message = process_file_by_type(file_path, file_extension, ocr_settings)

        # Add API-specific metadata
        result['filename'] = filename
        result['message'] = message
        result['api_version'] = 'v1'
        result['processing_time'] = None  # Could be enhanced later with timing

        return jsonify(result), 200

    except ValueError as e:
        error_message = str(e)
        if 'not supported' in error_message:
            return jsonify({'error': 'Unsupported file type', 'message': error_message}), 400
        return jsonify({'error': 'Processing failed', 'message': error_message}), 422
    except OSError as e:
        return jsonify({
            'error': 'File save failed',
            'message': f'Unable to save file: {str(e)}'
        }), 500


@app.route('/api/v1/formats', methods=['GET'])
def api_formats():
    """
    REST API endpoint to get supported file formats

    Returns:
        JSON response with list of supported file extensions and descriptions
    """
    format_descriptions = {
        'png': 'Portable Network Graphics - Lossless image format',
        'jpg': 'JPEG - Compressed image format',
        'jpeg': 'JPEG - Compressed image format',
        'pdf': 'Portable Document Format - Multi-page documents',
        'docx': 'Microsoft Word Document - Text documents',
        'txt': 'Plain Text File - Simple text documents',
        'csv': 'Comma-Separated Values - Spreadsheet data',
        'xls': 'Microsoft Excel Spreadsheet - Legacy Excel format',
        'xlsx': 'Microsoft Excel Spreadsheet - Modern Excel format'
    }

    formats = []
    for ext in config.ALLOWED_EXTENSIONS:
        formats.append({
            'extension': ext,
            'description': format_descriptions.get(ext, f'{ext.upper()} file format'),
            'ocr_supported': ext in ['png', 'jpg', 'jpeg', 'pdf']
        })

    return jsonify({
        'supported_formats': formats,
        'total_formats': len(formats),
        'api_version': 'v1'
    }), 200


@app.route('/api/v1/languages', methods=['GET'])
def api_languages():
    """
    REST API endpoint to get available OCR languages

    Returns:
        JSON response with available language codes and names
    """
    try:
        available_langs = get_available_languages()
        languages = []

        for lang_code in available_langs:
            languages.append({
                'code': lang_code,
                'name': config.AVAILABLE_LANGUAGES.get(lang_code, lang_code),
                'available': True
            })

        # Add configured languages that might not be installed
        for lang_code, lang_name in config.AVAILABLE_LANGUAGES.items():
            if lang_code not in available_langs:
                languages.append({
                    'code': lang_code,
                    'name': lang_name,
                    'available': False
                })

        return jsonify({
            'languages': languages,
            'installed_count': len(available_langs),
            'total_configured': len(config.AVAILABLE_LANGUAGES),
            'api_version': 'v1'
        }), 200

    except (RuntimeError, ValueError, OSError) as e:
        return jsonify({
            'error': 'Language detection failed',
            'message': str(e),
            'api_version': 'v1'
        }), 500


@app.route('/api/v1/health', methods=['GET'])
def api_health():
    """
    REST API endpoint for service health check

    Returns:
        JSON response with service status and capabilities
    """
    try:
        # Check OCR availability
        ocr_status = 'available' if OCR_AVAILABLE else 'unavailable'

        # Get basic system info
        health_info = {
            'status': 'healthy',
            'api_version': 'v1',
            'ocr_engine': {
                'available': OCR_AVAILABLE,
                'status': ocr_status
            },
            'supported_formats': len(config.ALLOWED_EXTENSIONS),
            'pdf_processing': PDF_TEXT_EXTRACTION_AVAILABLE,
            'upload_folder': os.path.exists(config.UPLOAD_FOLDER),
            'max_file_size_mb': config.MAX_CONTENT_LENGTH // (1024 * 1024)
        }

        # Add Tesseract version if available
        if OCR_AVAILABLE:
            try:
                tesseract_version = pytesseract.get_tesseract_version()
                health_info['ocr_engine']['version'] = str(tesseract_version)
            except (pytesseract.TesseractNotFoundError, RuntimeError):
                health_info['ocr_engine']['version'] = 'unknown'

        return jsonify(health_info), 200

    except (RuntimeError, ValueError, OSError) as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'api_version': 'v1'
        }), 500


@app.route('/api/v1/docs', methods=['GET'])
def api_docs():
    """
    REST API endpoint for comprehensive API documentation

    Returns:
        JSON response with complete API documentation
    """
    documentation = {
        'api_version': 'v1',
        'title': 'Docusense OCR API',
        'description': 'Local-first OCR service with advanced processing capabilities',
        'base_url': '/api/v1',
        'endpoints': {
            'POST /api/v1/ocr': {
                'description': 'Upload and process files with OCR',
                'parameters': {
                    'file': {
                        'type': 'file',
                        'required': True,
                        'description': 'File to process (image, PDF, document, or spreadsheet)'
                    },
                    'dpi_setting': {
                        'type': 'string',
                        'required': False,
                        'default': 'medium',
                        'options': ['low', 'medium', 'high'],
                        'description': 'DPI setting for OCR processing'
                    },
                    'language': {
                        'type': 'string',
                        'required': False,
                        'default': 'eng',
                        'description': 'Language code for OCR (eng, fra, deu, spa, etc.)'
                    },
                    'engine_mode': {
                        'type': 'string',
                        'required': False,
                        'default': 'combined',
                        'options': ['legacy', 'lstm', 'combined', 'default'],
                        'description': 'OCR engine mode'
                    },
                    'psm_mode': {
                        'type': 'string',
                        'required': False,
                        'default': 'auto',
                        'description': 'Page segmentation mode'
                    }
                },
                'response': {
                    'success': {
                        'data': 'OCR results with text and bounding boxes',
                        'filename': 'Original filename',
                        'message': 'Processing status message',
                        'ocr_settings': 'Applied OCR settings'
                    },
                    'error': {
                        'error': 'Error type',
                        'message': 'Error description'
                    }
                },
                'status_codes': {
                    '200': 'Success - File processed successfully',
                    '400': 'Bad Request - Invalid file type or missing file',
                    '422': 'Unprocessable Entity - Processing failed',
                    '500': 'Internal Server Error - Server error'
                }
            },
            'GET /api/v1/formats': {
                'description': 'Get supported file formats',
                'parameters': {},
                'response': {
                    'supported_formats': 'List of format objects with extension and description',
                    'total_formats': 'Total number of supported formats'
                },
                'status_codes': {
                    '200': 'Success - Formats retrieved'
                }
            },
            'GET /api/v1/languages': {
                'description': 'Get available OCR languages',
                'parameters': {},
                'response': {
                    'languages': 'List of language objects with code, name, and availability',
                    'installed_count': 'Number of installed language packs',
                    'total_configured': 'Total configured languages'
                },
                'status_codes': {
                    '200': 'Success - Languages retrieved',
                    '500': 'Internal Server Error - Language detection failed'
                }
            },
            'GET /api/v1/health': {
                'description': 'Check service health and capabilities',
                'parameters': {},
                'response': {
                    'status': 'Service health status',
                    'ocr_engine': 'OCR engine availability and version',
                    'supported_formats': 'Number of supported formats',
                    'pdf_processing': 'PDF processing capability',
                    'upload_folder': 'Upload folder status'
                },
                'status_codes': {
                    '200': 'Success - Service is healthy',
                    '500': 'Internal Server Error - Service has issues'
                }
            },
            'GET /api/v1/docs': {
                'description': 'Get API documentation',
                'parameters': {},
                'response': 'Complete API documentation in JSON format',
                'status_codes': {
                    '200': 'Success - Documentation retrieved'
                }
            }
        },
        'examples': {
            'curl_upload': ('curl -X POST -F "file=@document.pdf" -F "language=eng" '
                           '-F "dpi_setting=medium" http://localhost:5000/api/v1/ocr'),
            'curl_health': 'curl http://localhost:5000/api/v1/health',
            'curl_formats': 'curl http://localhost:5000/api/v1/formats',
            'curl_languages': 'curl http://localhost:5000/api/v1/languages'
        },
        'error_codes': {
            'unsupported_file_type': 'File extension not supported',
            'processing_failed': 'OCR or file processing failed',
            'file_save_failed': 'Unable to save uploaded file',
            'no_file_provided': 'No file included in request',
            'language_detection_failed': 'Unable to detect available languages'
        }
    }

    return jsonify(documentation), 200


@app.route('/api-test')
def api_test_interface():
    """
    Simple API testing interface

    Returns:
        Basic HTML page for testing API endpoints
    """
    return '''<html><head><title>API Test</title></head><body>
    <h1>API Testing</h1>
    <div><h2>Health Check</h2><button onclick="fetch('/api/v1/health').then(r=>r.json()).then(d=>document.getElementById('h').innerText=JSON.stringify(d,null,2))">Test</button><pre id="h"></pre></div>
    <div><h2>Formats</h2><button onclick="fetch('/api/v1/formats').then(r=>r.json()).then(d=>document.getElementById('f').innerText=JSON.stringify(d,null,2))">Test</button><pre id="f"></pre></div>
    <div><h2>Languages</h2><button onclick="fetch('/api/v1/languages').then(r=>r.json()).then(d=>document.getElementById('l').innerText=JSON.stringify(d,null,2))">Test</button><pre id="l"></pre></div>
    <div><h2>OCR Upload</h2><form onsubmit="event.preventDefault();let f=new FormData();f.append('file',this.file.files[0]);f.append('dpi_setting','medium');f.append('language','eng');fetch('/api/v1/ocr',{method:'POST',body:f}).then(r=>r.json()).then(d=>document.getElementById('o').innerText=JSON.stringify(d,null,2))"><input name="file" type="file"><button type="submit">Upload</button></form><pre id="o"></pre></div>
    <div><h2>Documentation</h2><button onclick="fetch('/api/v1/docs').then(r=>r.json()).then(d=>document.getElementById('d').innerText=JSON.stringify(d,null,2))">Test</button><pre id="d"></pre></div>
    </body></html>'''


if __name__ == '__main__':
    # Run the Flask application in development mode
    app.run(
        debug=config.DEBUG,
        threaded=config.THREADED,
        host=config.HOST,
        port=config.PORT
    )
