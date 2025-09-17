# Docusense - Advanced Local OCR Service

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/Flask-2.x-orange.svg)](https://flask.palletsprojects.com/)
[![Tesseract](https://img.shields.io/badge/Tesseract-OCR-red.svg)](https://github.com/tesseract-ocr/tesseract)

**A comprehensive, local-first OCR service with advanced settings, multi-format support, and REST API integration.**

**Status:** ⏳ **Extended Prototype** - Full-featured OCR service with 6 core file format support, advanced settings, and REST API.

---

## 🎯 System Overview

This project is a comprehensive Optical Character Recognition (OCR) service that runs entirely on your local machine. It provides both a web interface and REST API for processing 6 core document formats with advanced OCR settings and multi-language support.

### 🌟 **Key Features**

**📄 Multi-Format File Support (6 Core Types)**
- **Images**: PNG, JPG, JPEG
- **Documents**: PDF (enhanced multi-page processing), DOCX, TXT
- **Spreadsheets**: CSV, XLS, XLSX

**🔧 Advanced OCR Configuration**
- **Multi-Language Support**: Process documents in multiple languages using Tesseract language packs
- **DPI Settings**: Configurable resolution (150, 300, 600 DPI) for optimal accuracy
- **OCR Engine Parameters**: Advanced settings for engine mode, page segmentation, and character filtering

**🌐 Simple REST API Integration**
- **REST API**: `/api/v1/` endpoints for programmatic access
- **No Authentication**: Simple access without API keys for prototype usage
- **API Documentation**: Interactive documentation and testing interface
- **Easy Integration**: Straightforward HTTP endpoints for external applications

**💻 Enhanced Web Interface**
- **Advanced Settings Panel**: Configure all OCR parameters through the UI
- **Real-time Preview**: Interactive canvas with text region highlighting
- **Multi-format Processing**: Seamless handling of all supported file types
- **Structured Output**: Comprehensive JSON export with processing metadata

## 🚀 Quick Start

### Prerequisites
Before you begin, ensure you have the following installed on your Windows machine:
- **Python 3.9+**: Make sure to check 'Add Python to PATH' during installation.
- **Tesseract OCR**: Install the UB-Mannheim build and add the installation folder (e.g., `C:\Program Files\Tesseract-OCR`) to your system's PATH.
- **Tesseract Language Packs**: Install additional language packs for multi-language OCR support (optional but recommended).
- **Poppler**: Download the Windows binaries, unzip them, and add the `\Library\bin` sub-folder to your system's PATH. Required for PDF processing.

### System Requirements
- **OS**: Windows 10/11
- **RAM**: 4GB+ recommended (higher for large documents and high DPI processing)
- **Storage**: 1GB free space for dependencies and temporary files
- **Network**: None required (fully local operation)

### Installation
```powershell
# 1. Clone the repository
git clone https://github.com/username/docusense-ai.git
cd docusense-ai

# 2. Create the required directories
mkdir uploads
mkdir templates

# 3. Create a virtual environment and activate it
python -m venv venv
.\venv\Scripts\Activate.ps1

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Configure the system (optional)
# Edit config.py to customize DPI settings, API keys, and other parameters
```

### Running the System
```powershell
# 1. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run the Flask application
python app.py
```
After running the command:
- **Web Interface**: Open your web browser and navigate to **`http://127.0.0.1:5000`**
- **API Documentation**: Access API docs at **`http://127.0.0.1:5000/api/v1/docs`**
- **API Testing Interface**: Try the API at **`http://127.0.0.1:5000/api-test`**

## 🧪 How to Test

### **Web Interface Testing**
1. **Basic Functionality**: Run `python app.py` and open `http://127.0.0.1:5000`
2. **File Format Testing**: Upload files with all supported extensions:
   - **Images**: `.png`, `.jpg`, `.jpeg`
   - **Documents**: `.pdf` (test multi-page), `.docx`, `.txt`
   - **Spreadsheets**: `.csv`, `.xls`, `.xlsx`
3. **Advanced OCR Settings**: Test different DPI settings, languages, and engine parameters
4. **Visual Verification**: Check image preview with bounding boxes and canvas overlay
5. **Data Export**: Verify "Plain Text", "Structured JSON", and download functionality
6. **Error Handling**: Try unsupported files and invalid configurations

### **API Testing**
1. **API Health Check**: `GET http://127.0.0.1:5000/api/v1/health`
2. **File Processing**: `POST http://127.0.0.1:5000/api/v1/ocr` with file upload
3. **Information Endpoints**:
   - `GET /api/v1/formats` - supported file formats
   - `GET /api/v1/languages` - available OCR languages
4. **Documentation**: Access `/api/v1/docs` and `/api-test` for comprehensive testing
5. **Simple Access**: All endpoints work without authentication for easy testing

For detailed test cases, see **[Testing Guide](docs/Testing_Guide.md)**.

## 🛠️ System Architecture

The application is a comprehensive monolithic service with dual interfaces:

```
docusense-ai/
├── app.py                 # Main Flask application with web routes and API endpoints
├── config.py              # Central configuration management
├── templates/
│   └── index.html         # Enhanced frontend with advanced settings
├── uploads/               # Directory for storing uploaded and processed files
├── docs/                  # Comprehensive documentation
├── requirements.txt       # Extended Python dependencies
└── README.md              # This file
```

### **Architecture Components**
- **Web Interface**: Enhanced HTML/CSS/JavaScript frontend with advanced OCR controls
- **REST API**: Full `/api/v1/` endpoint suite for programmatic access
- **OCR Processing Engine**: Multi-format document processing with configurable parameters
- **Authentication Layer**: API key-based security with rate limiting
- **Configuration System**: Centralized settings management in `config.py`
- **File Processing Pipeline**: Support for 15+ document and image formats

## 🔧 API Reference

### **Web Interface Endpoints**
- `GET /`: Main web interface for file upload and OCR processing
- `POST /upload`: Web form file upload endpoint with OCR processing
- `GET /uploads/<filename>`: Static file serving for processed images

### **REST API Endpoints (`/api/v1/`)**
- `POST /api/v1/ocr`: **File Processing** - Upload and process files programmatically
- `GET /api/v1/formats`: **Supported Formats** - List all supported file extensions
- `GET /api/v1/languages`: **Available Languages** - List installed Tesseract language packs
- `GET /api/v1/health`: **Health Check** - Service status and version information
- `GET /api/v1/docs`: **API Documentation** - Comprehensive API reference

### **Development and Testing**
- `GET /api-test`: **API Testing Interface** - Interactive forms to test all endpoints

### **Simple API Access**
All `/api/v1/` endpoints are accessible without authentication for prototype usage.

### **Example API Usage**
```bash
# Health check
curl http://127.0.0.1:5000/api/v1/health

# Process a file
curl -F "file=@document.png" http://127.0.0.1:5000/api/v1/ocr

# Get supported formats
curl http://127.0.0.1:5000/api/v1/formats

# Get available languages
curl http://127.0.0.1:5000/api/v1/languages
```

## 📝 Documentation

- **[Project Master Context](docs/Project_Master_Context.md)** - System architecture and design.
- **[Project TODO List](docs/Project_TODO_List.md)** - Development priorities based on the implementation plan.
- **[Testing Guide](docs/Testing_Guide.md)** - Manual testing procedures.
- **[Development Guide](docs/Development_Guide.md)** - Development practices.
- **[Startup Guide](docs/STARTUP_GUIDE.md)** - System startup and configuration.

## 🛠️ Development

### Prerequisites for Development
- Python 3.9 or higher
- Tesseract OCR installed and configured
- Poppler utilities for PDF processing
- Virtual environment recommended

### Setting Up Development Environment
```powershell
# 1. Clone and navigate to the repository
git clone https://github.com/username/docusense-ai.git
cd docusense-ai

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

### Code Quality Standards
- **Pylint Score**: Maintained at 10.0/10.0 for `app.py`
- **PEP 8 Compliance**: All Python code follows PEP 8 standards
- **Error Handling**: Specific exceptions used (no generic `Exception` blocks)
- **Documentation**: Clear comments for all logical code blocks

## 🤝 Contributing

This is currently a prototype project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows the existing style and quality standards
- All tests pass (maintain pylint 10.0/10.0 score)
- Documentation is updated as needed

## 🔐 Security

**Important**: This is a prototype application designed for local use only:
- No production-grade security features
- Not suitable for internet-facing deployment
- No authentication mechanisms
- Use only in trusted, local environments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Testing**: Follow the [Testing Guide](docs/Testing_Guide.md) for validation procedures

## 🔄 Project Status

**Current Phase**: Extended Prototype with 6 core file formats
- ✅ Basic OCR functionality
- ✅ Multi-format support (Images, PDFs, Documents, Spreadsheets)
- ✅ Advanced OCR settings (DPI, Language, Engine parameters)
- ✅ REST API endpoints
- ✅ Enhanced web interface
- 🚧 Production readiness features (future scope)

For detailed development progress, see [Project TODO List](docs/Project_TODO_List.md).