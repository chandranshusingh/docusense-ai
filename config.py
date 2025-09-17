# Configuration file for Docusense OCR Prototype
# All constants, paths, and configuration values are managed here

# Flask Configuration
DEBUG = True
THREADED = True
HOST = '127.0.0.1'
PORT = 5000

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Supported File Extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'txt', 'csv', 'xls', 'xlsx'}

# OCR Configuration - Multiple possible Tesseract paths
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',  # Standard installation path
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',  # 32-bit path
    'tesseract.exe',  # If in PATH
    r'C:\tesseract\tesseract.exe'  # Alternative location
]
POPPLER_PATH = r'C:\poppler-23.11.0\Library\bin'  # Default Windows path for Poppler

# File Processing Configuration
PDF_DPI = 300  # DPI for PDF to image conversion
PROCESS_FIRST_PAGE_ONLY = False  # Process all pages for enhanced PDF processing

# Enhanced PDF Processing Configuration
MAX_PDF_PAGES = 10  # Maximum number of pages to process to avoid memory issues
PDF_TEXT_EXTRACTION_FIRST = True  # Try text extraction before OCR for text-based PDFs

# Spreadsheet Processing Configuration
CSV_DELIMITER = ','  # Default delimiter for CSV files
CSV_ENCODING = 'utf-8'  # Default encoding for CSV files
EXCEL_MAX_ROWS = 1000  # Maximum rows to process from Excel files
EXCEL_MAX_COLUMNS = 50  # Maximum columns to process from Excel files

# Advanced OCR Configuration - DPI Settings
DPI_PRESETS = {
    'low': 150,      # Fast processing, lower accuracy
    'medium': 300,   # Balanced processing and accuracy (default)
    'high': 600      # Slower processing, higher accuracy
}
DEFAULT_DPI_SETTING = 'medium'

# Advanced OCR Configuration - Language Support
AVAILABLE_LANGUAGES = {
    'eng': 'English',
    'fra': 'French',
    'deu': 'German',
    'spa': 'Spanish',
    'ita': 'Italian',
    'por': 'Portuguese',
    'rus': 'Russian',
    'chi_sim': 'Chinese (Simplified)',
    'chi_tra': 'Chinese (Traditional)',
    'jpn': 'Japanese',
    'kor': 'Korean',
    'ara': 'Arabic',
    'hin': 'Hindi'
}
DEFAULT_LANGUAGE = 'eng'

# Advanced OCR Configuration - Engine Parameters
OCR_ENGINE_MODES = {
    'legacy': 0,     # Legacy engine only
    'lstm': 1,       # Neural nets LSTM engine only
    'combined': 2,   # Legacy + LSTM engines (default)
    'default': 3     # Default, based on what is available
}
DEFAULT_OCR_ENGINE_MODE = 'lstm'

PAGE_SEGMENTATION_MODES = {
    'auto': 3,              # Fully automatic page segmentation (default)
    'single_column': 4,     # Assume a single column of text of variable sizes
    'single_uniform': 6,    # Assume a single uniform block of vertically aligned text
    'single_text_line': 7,  # Treat the image as a single text line
    'single_word': 8,       # Treat the image as a single word
    'circle_word': 9,       # Treat the image as a single word in a circle
    'single_char': 10,      # Treat the image as a single character
    'sparse_text': 11,      # Sparse text. Find as much text as possible
    'sparse_osd': 12,       # Sparse text with OSD
    'raw_line': 13          # Raw line. Treat the image as a single text line
}
DEFAULT_PSM_MODE = 'single_column'  # Better text recognition for ID cards

# Output Configuration
JSON_FILENAME = 'extracted_data.json'
