# Development Guide - Docusense OCR Prototype

**Document Purpose**: A simple guide to developing the OCR prototype.
**Version**: 0.1.0 (Prototype)
**Status**: ✅ **ACTIVE DEVELOPMENT**

---

## 🚀 **QUICK START**

### **Environment Setup**
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Install dependencies (if you haven't already)
pip install -r requirements.txt

# 3. Start the application
python app.py
```
Open `http://127.0.0.1:5000` in your browser to see the application.

---

## 🛠️ **DEVELOPMENT ENVIRONMENT**

### **Technology Stack**
- **Backend**: Python 3.9+ with Flask
- **Frontend**: HTML5, Tailwind CSS, vanilla JavaScript
- **OCR**: Tesseract (via `pytesseract`)
- **File Processing**: `Pillow`, `pdf2image`, `python-docx`
- **OS**: Windows 10/11

### **Port Configuration**
- **Application Server**: Port 5000 (Flask development server)

---

## 📁 **PROJECT STRUCTURE**

The project structure is intentionally simple for this prototype.

```
docusense-ai/
├── app.py                 # The complete backend logic in a single Flask file.
├── templates/
│   └── index.html         # The complete frontend in a single HTML file.
├── uploads/               # Stores files uploaded by the user.
├── requirements.txt       # Python dependencies.
├── docs/                  # Project documentation.
└── README.md              # Project overview.
```

---

## 🔧 **DEVELOPMENT WORKFLOW**

The development cycle for this prototype is straightforward:

1.  **Activate Environment**: Always start by activating the virtual environment: `.\venv\Scripts\Activate.ps1`.
2.  **Run the Server**: Start the Flask server with `python app.py`. The server will automatically reload when you save changes to `app.py`.
3.  **Make Code Changes**:
    *   For backend logic, edit `app.py`.
    *   For frontend UI or logic, edit `templates/index.html`.
4.  **Test Changes**:
    *   If you changed `app.py`, the server will restart automatically.
    *   If you changed `templates/index.html`, simply refresh your browser.
    *   Manually test the feature you've added or modified. Refer to the `docs/Testing_Guide.md` for manual test cases.

### **Code Style**

While this is a prototype, try to maintain clean code:
- Use clear variable and function names.
- Add comments to explain complex parts of the logic (e.g., the canvas scaling calculations).
- Keep functions small and focused on a single task.

### **Debugging Workflow**

#### **Backend Debugging (`app.py`)**
- The Flask development server is run in **debug mode** by default. This provides a rich, interactive debugger in your browser if an error occurs on the backend.
- Use `print()` statements in `app.py` to inspect variables. The output will appear in the terminal where the server is running.

#### **Frontend Debugging (`index.html`)**
- Use your web browser's built-in Developer Tools (usually opened with `F12`).
- The **Console** tab is essential for viewing `console.log()` outputs and seeing JavaScript errors.
- The **Network** tab is useful for inspecting the request to the `/upload` endpoint and seeing the JSON response from the server.
---