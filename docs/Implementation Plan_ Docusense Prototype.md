# **Implementation Plan: Local OCR Service Prototype**

## **1\. Project Overview**

This document outlines the step-by-step plan to build a local OCR (Optical Character Recognition) service prototype. The service will feature a web-based UI for uploading documents (images, PDFs, DOCX, TXT, CSV, XLS/XLSX) and a Python backend to perform the OCR with advanced settings, display results with highlighted text, generate structured JSON data, and provide REST API endpoints for external integration.

**Technology Stack:**

* **Backend:** Python with Flask  
* **OCR Engine:** Tesseract OCR with language pack support
* **Frontend:** HTML, Tailwind CSS, JavaScript  
* **File Handling:** Pillow (for images), pdf2image (for enhanced PDF processing), python-docx (for Word documents), pandas and openpyxl (for spreadsheet processing)
* **API:** Simple RESTful endpoints for programmatic access

## **Phase 1: Environment Setup & Prerequisites**

This phase ensures your local Windows machine is ready for development.

### **Step 1.1: Install Required Software**

**Goal:** Install Python, the Tesseract OCR engine, and the Poppler PDF utility.

**Prompt for Claude Sonnet:**

"Provide a concise, step-by-step guide for a Windows user to install the following software required for a local OCR project:

1. **Python 3.9+:** Include a link to the official download page and emphasize the importance of checking 'Add Python to PATH' during installation.  
2. **Tesseract OCR:** Provide a link to the recommended Windows installer from the UB-Mannheim GitHub repository. Explain how to add the Tesseract installation directory (e.g., C:\\Program Files\\Tesseract-OCR) to the Windows System PATH environment variable.  
3. **Poppler:** Provide a link to a reliable source for Windows binaries (e.g., the https://www.google.com/search?q=alivate.com.au blog). Explain how to unzip it and add its \\Library\\bin sub-folder to the Windows System PATH environment variable."

### **Step 1.2: Set Up Project Directory Structure**

**Goal:** Create the necessary folders for the project.

**Prompt for Claude Sonnet:**

"Show the command-line instructions to create the following directory structure for a new project named ocr-service:

ocr-service/  
|-- app.py  
|-- templates/  
|   |-- index.html  
|-- uploads/

Also, provide the commands to create the empty files app.py and index.html within their respective directories."

### **Step 1.3: Install Python Dependencies**

**Goal:** Install all required Python packages using pip.

**Prompt for Claude Sonnet:**

"Generate a single pip install command to install all of the following Python libraries: Flask, pytesseract, Pillow, pdf2image, and python-docx."

## **Phase 2: Backend Development (app.py)**

This phase focuses on building the core logic of the OCR service.

### **Step 2.1: Create the Basic Flask Application**

**Goal:** Set up a minimal, runnable Flask server.

**Prompt for Claude Sonnet:**

"Generate the foundational Python code for app.py.  
This script should:

1. Import necessary modules: os, Flask, render\_template.  
2. Initialize a Flask app.  
3. Define a configuration variable UPLOAD\_FOLDER and set it to 'uploads'.  
4. Use the os module to create the upload folder if it doesn't already exist.  
5. Define a root route / that uses render\_template to serve index.html.  
6. Include the standard if \_\_name\_\_ \== '\_\_main\_\_': block to run the app in debug and threaded mode."

### **Step 2.2: Implement the File Upload Endpoint**

**Goal:** Create a /upload route to handle POST requests with file data.

**Prompt for Claude Sonnet:**

"Modify the app.py Flask script. Add a new route /upload that accepts POST requests.  
This route's function, named upload\_file, should:

1. Import request and jsonify from Flask.  
2. Perform initial validation: check if 'file' is in request.files and if the filename is not empty. Return a JSON error message with a 400 status code if validation fails.  
3. Define a helper function allowed\_file(filename) that checks if the file extension is one of: png, jpg, jpeg, pdf, docx, txt.  
4. If the file is valid and allowed, save it to the UPLOAD\_FOLDER.  
5. For now, return a simple JSON success message: jsonify({'message': 'File uploaded successfully', 'filename': filename})."

### **Step 2.3: Add Image and PDF Processing Logic**

**Goal:** Integrate Tesseract and Poppler to extract data from image and PDF files.

**Prompt for Claude Sonnet:**

"Update the app.py script by creating two new functions for OCR processing:

1. A function process\_image(filepath) that takes a file path, opens it using Pillow, and runs pytesseract.image\_to\_data on it. It should return the resulting data dictionary.  
2. A function process\_pdf(filepath) that uses pdf2image.convert\_from\_path to convert the first page of a PDF into an image. **Crucially, specify the Windows poppler\_path, for example: r'C:\\poppler-23.11.0\\Library\\bin'.** The function should save this new image to the uploads folder, then call process\_image on it, and finally return both the new image's filename and the OCR data.

Now, modify the /upload route. After saving the file, check its extension. If it's an image, call process\_image. If it's a PDF, call process\_pdf. Return the OCR data in the final JSON response."

### **Step 2.4: Add DOCX and TXT Processing Logic**

**Goal:** Add functions to extract text from text-based documents.

**Prompt for Claude Sonnet:**

"Further update app.py by adding two new functions for text extraction:

1. A function process\_docx(filepath) that uses the docx library to open a .docx file and extract all text from its paragraphs, returning a single string.  
2. A function process\_txt(filepath) that opens and reads a .txt file, returning its content as a string.

Modify the /upload route to call these functions for .docx and .txt files. For these file types, the returned JSON should be structured differently, for example: {'data': {'text\_only': 'the extracted text'}}."

### **Step 2.5: Finalize the Upload Route and Add a File Server**

**Goal:** Clean up the OCR data and create a route to serve the processed images to the frontend.

**Prompt for Claude Sonnet:**

"Finalize the app.py script.

1. In the /upload route, after getting the OCR data from pytesseract, add a cleanup step. Iterate through the results and filter out any entries where the 'text' field is empty or just whitespace. This will make the final JSON cleaner.  
2. Add a new route /uploads/\<filename\> with a function uploaded\_file(filename). This route should use Flask's send\_from\_directory function to serve files from the UPLOAD\_FOLDER. This is essential so the frontend \<img\> tag can access the uploaded or converted images."

## **Phase 3: Frontend Development (index.html)**

This phase focuses on creating the user interface for interacting with the service.

### **Step 3.1: Create the Basic HTML Structure**

**Goal:** Design the main layout of the web page using HTML and Tailwind CSS.

**Prompt for Claude Sonnet:**

"Generate the complete HTML code for templates/index.html.  
The page should be titled 'Local OCR Service' and use the Inter font. It must include the Tailwind CSS CDN link.  
The layout should have:

1. A main header with the title and a brief description.  
2. An 'Upload' section containing a styled file input and a submit button.  
3. A 'Results' section, initially hidden, that will contain the preview and extracted data. This section should have a 'Review' subsection for the image preview and a 'Get Extracted Data' subsection for the text/JSON outputs.  
4. Style the page with a clean, modern aesthetic using gray backgrounds, white cards with shadows, and blue accent colors for buttons."

### **Step 3.2: Implement the JavaScript Upload Logic**

**Goal:** Write JavaScript to capture the form submission, send the file to the backend, and handle the response.

**Prompt for Claude Sonnet:**

"Inside the templates/index.html file, add a \<script\> tag at the end of the \<body\>.  
Write the JavaScript code to:

1. Get references to the form, file input, loader element, and results section.  
2. Add an event listener to the form's submit event. Prevent the default form submission.  
3. Inside the listener, show a loading indicator and hide any previous results or errors.  
4. Create a FormData object and append the selected file to it.  
5. Use the fetch API to send a POST request to the /upload endpoint with the FormData.  
6. Handle the JSON response from the server. If the response is not 'ok' or contains an error, display an error message. Otherwise, call a (currently empty) function named displayResults(result).  
7. Ensure the loading indicator is hidden after the request completes, regardless of success or failure."

### **Step 3.3: Implement Result Display with Canvas**

**Goal:** Display the uploaded image and draw the OCR bounding boxes over it.

**Prompt for Claude Sonnet:**

"Continuing in the \<script\> tag of index.html, implement the displayResults(result) function.  
The function must:

1. Unhide the main results section.  
2. Check if the result data is text\_only (for DOCX/TXT). If so, display that text in a designated \<pre\> tag and hide the image preview area.  
3. If the result contains image data:  
   a. Set the src of an \<img\> tag to /uploads/ \+ the filename from the result.  
   b. In the img.onload event handler, get a reference to a \<canvas\> element.  
   c. Resize the canvas to match the displayed size of the image (clientWidth, clientHeight).  
   d. Calculate the scaling factor between the image's natural dimensions and its displayed dimensions.  
   e. Iterate through the bounding box data (left, top, width, height) from the JSON result.  
   f. For each box, use the scaling factor to draw a semi-transparent, red-filled rectangle on the canvas at the correct position."

### **Step 3.4: Populate Outputs and Add JSON Download**

**Goal:** Fill the text areas with the extracted data and enable downloading the JSON.

**Prompt for Claude Sonnet:**

"Complete the JavaScript in index.html.

1. Inside the displayResults function, after processing the bounding boxes, generate the full plain text by joining all the 'text' items from the data. Set this as the value of the 'Plain Text' \<textarea\>.  
2. Format the detailed OCR data into a structured JSON array. Each object in the array should contain the text, confidence, and box coordinates.  
3. Use JSON.stringify with pretty-printing (3rd argument set to 2\) to format this JSON and set it as the value of the 'Structured JSON' \<textarea\>.  
4. Add a 'click' event listener to a 'Download JSON' button. When clicked, it should create a Blob from the content of the JSON textarea, generate an object URL for it, and trigger a browser download for a file named extracted\_data.json."

## **Phase 4: Running the Application**

### **Step 4.1: Launch and Test**

**Goal:** Run the Flask server and test the full application flow.

**Prompt for Claude Sonnet:**

"Provide the final command to run the Flask application from the terminal. Also, specify the local URL (e.g., http://127.0.0.1:5000) that the user should open in their web browser to access the OCR service."

## **Phase 5: Extended File Format Support**

This phase extends the prototype to support additional file formats for data extraction, focusing on spreadsheet formats and enhanced PDF processing.

### **Step 5.1: Enhanced PDF Processing**

**Goal:** Improve PDF processing capabilities for better text extraction and multi-page handling.

**Prompt for Claude Sonnet:**

"Enhance the PDF processing capabilities in app.py:

1. Update the process_pdf() function to handle multi-page PDFs (process all pages, not just the first).
2. Add support for both text-based PDFs (direct text extraction) and image-based PDFs (OCR processing).
3. Implement page-by-page processing with consolidated results.
4. Add proper error handling for password-protected or corrupted PDF files.
5. Include page information in the JSON response structure."

### **Step 5.2: Add Support for CSV and Excel Files**

**Goal:** Enable text extraction from spreadsheet files for data processing and text content extraction.

**Prompt for Claude Sonnet:**

"Add spreadsheet processing capabilities to app.py:

1. Install pandas and openpyxl for Excel file handling.
2. Create a process_csv(filepath) function that reads CSV content and formats it as structured text.
3. Create a process_excel(filepath) function that extracts text from all sheets in Excel files (.xls, .xlsx).
4. Update the allowed_file() function to include 'csv', 'xls', 'xlsx' extensions.
5. Format the output to maintain table structure in the plain text representation.
6. Handle empty cells and merged cells appropriately.
7. Return structured data similar to other text-based formats (text_only format)."

## **Phase 6: Advanced OCR Settings**

This phase adds configurable OCR settings to improve accuracy and support multiple languages.

### **Step 6.1: Implement DPI Configuration**

**Goal:** Allow users to specify DPI settings for better OCR accuracy on different image qualities.

**Prompt for Claude Sonnet:**

"Add DPI configuration support to the OCR processing:

1. Add DPI configuration options to config.py with default values (300, 150, 600 DPI presets).
2. Modify the frontend to include a DPI selection dropdown in the upload form.
3. Update the process_image() function to accept DPI parameter and use it with pytesseract.image_to_data().
4. Add image preprocessing logic to resize/resample images based on the selected DPI.
5. Include DPI information in the returned JSON response for reference."

### **Step 6.2: Add Language Pack Support**

**Goal:** Enable OCR processing in multiple languages using Tesseract language packs.

**Prompt for Claude Sonnet:**

"Implement multi-language OCR support:

1. Add language configuration to config.py with common language codes (eng, fra, deu, spa, etc.).
2. Create a function get_available_languages() that detects installed Tesseract language packs.
3. Add a language selection dropdown to the frontend upload form.
4. Modify OCR processing functions to use the lang parameter with pytesseract.
5. Update the JSON response to include the language used for processing.
6. Add error handling for missing language packs with user-friendly messages."

### **Step 6.3: Implement OCR Engine Parameters**

**Goal:** Provide advanced OCR configuration options for fine-tuning recognition accuracy.

**Prompt for Claude Sonnet:**

"Add advanced OCR parameter configuration:

1. Add OCR engine mode and page segmentation mode options to config.py.
2. Create a function get_tesseract_config() that generates pytesseract configuration strings.
3. Add an 'Advanced Settings' section to the frontend with options for:
   - OCR Engine Mode (Legacy, LSTM, Combined)
   - Page Segmentation Mode (Auto, Single block, Single line, etc.)
   - Character whitelist/blacklist
4. Update OCR processing to use these advanced parameters.
5. Provide tooltips or help text explaining each advanced option."

## **Phase 7: REST API Endpoints**

This phase creates RESTful API endpoints for programmatic access to the OCR service.

### **Step 7.1: Create Core API Endpoints**

**Goal:** Implement REST API endpoints for file upload and processing.

**Prompt for Claude Sonnet:**

"Create RESTful API endpoints in app.py:

1. Create a new API blueprint or route prefix '/api/v1/'.
2. Implement POST /api/v1/ocr endpoint that accepts file uploads and returns JSON results.
3. Implement GET /api/v1/formats to return supported file formats.
4. Implement GET /api/v1/languages to return available OCR languages.
5. Implement GET /api/v1/health endpoint for basic service health checks.
6. Add proper HTTP status codes (200, 400, 422, 500) and error response formatting.
7. Include API versioning in the URL structure for future compatibility."

### **Step 7.2: Create API Documentation and Testing Endpoints**

**Goal:** Provide comprehensive API documentation and testing capabilities.

**Prompt for Claude Sonnet:**

"Create API documentation and testing features:

1. Implement GET /api/v1/docs endpoint that returns API documentation in JSON format.
2. Create a simple API testing interface at /api-test with forms to test each endpoint.
3. Add basic API documentation generation for all endpoints with request/response examples.
4. Add error code explanations and troubleshooting information.
5. Include usage examples for each endpoint in the documentation.
6. Create a simple testing page that demonstrates API usage without authentication requirements."