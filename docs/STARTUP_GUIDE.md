# Startup Guide - Docusense OCR Prototype

**Document Purpose**: System startup and configuration guide for the OCR prototype.
**Version**: 0.1.0 (Prototype)
**Status**: ✅ **OPERATIONAL** - Startup procedures are defined.

---

## 🚀 **QUICK START**

### **One-Command Startup**
```powershell
# Make sure your virtual environment is active first
# Then, run the application
python app.py
```
Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 🛠️ **PREREQUISITES**

### **System Requirements**
- **OS**: Windows 10/11
- **Python**: 3.9+

### **Required Software**
- **Tesseract OCR**: The OCR engine must be installed and its installation directory added to the system PATH.
- **Poppler**: Required for PDF processing. The `\Library\bin` folder from its installation must be added to the system PATH.

### **Environment Setup**
```powershell
# 1. Create a virtual environment (if you haven't already)
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🔧 **STARTUP PROCEDURES**

### **Running the Application**

The application is a single Flask script.

#### **Steps**
1.  Navigate to the project's root directory in your terminal.
2.  Ensure your Python virtual environment is activated (`.\venv\Scripts\Activate.ps1`).
3.  Run the main application file:
    ```powershell
    python app.py
    ```

#### **Expected Output**
You will see output from Flask indicating that the server is running. It will look something like this:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ********
```

---

## 🔍 **HEALTH CHECKS**

### **Service Health Verification**
1.  **Check the Terminal**: Ensure the `python app.py` command is still running and has not crashed.
2.  **Open the Web Interface**: Navigate to `http://127.0.0.1:5000`. The "Local OCR Service" page should load correctly.
3.  **Test an Upload**: The most reliable health check is to upload a sample document and verify that you get a result. If this works, the service and its dependencies (Tesseract, Poppler) are correctly configured.

---

## 🚨 **TROUBLESHOOTING**

### **Common Startup Issues**

#### **1. `pytesseract.TesseractNotFoundError`**
- **Problem**: Python cannot find the Tesseract OCR engine.
- **Solution**: Ensure you have installed Tesseract OCR and that its installation directory (e.g., `C:\Program Files\Tesseract-OCR`) is correctly added to your Windows PATH environment variable. You may need to restart your terminal or PC for the new PATH to take effect.

#### **2. PDF Processing Fails or Hangs**
- **Problem**: The application fails when uploading a PDF. This is often caused by `pdf2image` not being able to find Poppler.
- **Solution**:
    1.  Ensure you have downloaded the Poppler binaries for Windows.
    2.  Confirm that the path to Poppler's `bin` directory (e.g., `C:\path\to\poppler-23.11.0\Library\bin`) is correctly added to your Windows PATH.
    3.  Alternatively, you can hardcode the path to Poppler inside the `process_pdf` function in `app.py` as a temporary fix.

#### **3. `ModuleNotFoundError`**
- **Problem**: Python cannot find a required library (e.g., Flask, Pillow).
- **Solution**: Make sure your virtual environment is activated and that you have installed all dependencies from `requirements.txt`.
    ```powershell
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

---

## 🛑 **SHUTDOWN PROCEDURES**

### **Graceful Shutdown**
- Press `CTRL+C` in the terminal where the Flask application (`app.py`) is running.

---