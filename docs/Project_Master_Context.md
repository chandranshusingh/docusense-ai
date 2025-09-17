# Project Master Context - Docusense OCR Prototype

**Document Purpose**: Central reference for the Docusense OCR Prototype development.
**Version**: 0.1.0 (Prototype)
**Status**: ⏳ **PROTOTYPE IN DEVELOPMENT**

---

## 🎯 System Overview

### Project Description
**Docusense OCR Prototype** is a comprehensive, self-contained service for performing Optical Character Recognition on various document types with advanced configuration options. It is designed to run locally without external dependencies, making it perfect for proof-of-concept validation. Users can upload files through a web interface or simple REST API and receive extracted plain text and structured data with bounding box coordinates, language detection, and configurable OCR parameters for optimal accuracy.

### Implementation Status Summary
- **Core System**: In development, following the phases outlined in the implementation plan.
- **Goal**: To create a functional prototype demonstrating the core OCR capabilities.
- **Scope**: Limited to local execution, no production-readiness features are included at this stage.

---

## 🏗️ System Architecture

### High-Level Architecture
The system is a simple, monolithic application composed of a frontend and a backend running in a single process.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Docusense OCR Prototype                        │
├─────────────────────────────────────────────────────────────────────┤
│  Frontend (Browser)      │  Backend (Flask Server @ localhost:5000)   │
│  ┌─────────────────────┐ │  ┌─────────────────────────────────────────┐ │
│  │  Web Interface      │ │  │         Flask App (`app.py`)            │ │
│  │ • HTML Structure    ├─► │  │ ──────────────────────────────────────── │ │
│  │ • Tailwind CSS      │ │  │ ► Web Routes                            │ │
│  │ • JavaScript        │ │  │   - `/` (Main Interface)                │ │
│  │   - File Upload     │ │  │   - `/upload` (File Processing)         │ │
│  │   - Advanced Settings│ │  │   - `/uploads/<name>` (File Serving)    │ │
│  │   - Canvas Display  │◄┤  │                                         │ │
│  │   - Results View    │ │  │ ► REST API Endpoints (`/api/v1/`)       │ │
│  └─────────────────────┘ │  │   - `/ocr` (Programmatic OCR)           │ │
│                          │  │   - `/formats` (Supported Formats)      │ │
│  External Apps           │  │   - `/languages` (Available Languages)   │ │
│  ┌─────────────────────┐ │  │   - `/health` (Service Health)          │ │
│  │  API Clients        │ │  │   - `/docs` (API Documentation)         │ │
│  │ • Postman/curl      ├─► │  │                                         │ │
│  │ • Custom Scripts    │ │  │ ► Enhanced OCR Processing               │ │
│  │ • Other Services    │ │  │   - Multi-format Support (6 formats)    │ │
│  └─────────────────────┘ │  │   - Advanced OCR Settings (DPI, Lang)   │ │
│                          │  │   - Language Pack Detection             │ │
│                          │  │   - Enhanced PDF Processing             │ │
│                          │  │   - Spreadsheet Data Extraction         │ │
│                          │  │                                         │ │
│                          │  │ ► Simple API Access                     │ │
│                          │  │   - No Authentication Required          │ │
│                          │  │   - Standard Error Handling             │ │
│                          │  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack
- **Backend**: Python 3.9+, Flask with API blueprints
- **OCR Engine**: Tesseract OCR (via `pytesseract`) with multi-language support
- **File Handling**:
  - Images: `Pillow` (PNG, JPG, JPEG)
  - PDFs: `pdf2image`, `Poppler` (dependency) with enhanced multi-page processing
  - Word Docs: `python-docx`
  - Spreadsheets: `pandas`, `openpyxl` (CSV, XLS, XLSX)
- **Frontend**: HTML5, Tailwind CSS, JavaScript (no framework)
- **API**: Simple RESTful endpoints for programmatic access
- **Development Environment**: Local Windows machine

---

## ✅ Core Features

### File Processing Capabilities
- **File Upload**: Web UI and REST API endpoints for file upload and processing
- **Multi-Format Support**: Handles 6 core document types:
  - **Images**: `png`, `jpg`, `jpeg`
  - **Documents**: `pdf` (enhanced multi-page processing), `docx`, `txt`
  - **Spreadsheets**: `csv`, `xls`, `xlsx`
- **OCR Processing**: Advanced text extraction from images and image-based PDFs using Tesseract
- **Enhanced PDF Processing**: Multi-page PDF support with both text extraction and OCR capabilities
- **Spreadsheet Processing**: Structured data extraction from CSV and Excel files

### Advanced OCR Features
- **Multi-Language Support**: OCR processing in multiple languages using Tesseract language packs
- **DPI Configuration**: Configurable DPI settings (150, 300, 600) for optimal OCR accuracy
- **OCR Engine Parameters**: Advanced settings including:
  - OCR Engine Mode (Legacy, LSTM, Combined)
  - Page Segmentation Mode options
  - Character whitelist/blacklist
  - Custom Tesseract parameters

### Visual and Data Features
- **Visual Feedback**: Interactive canvas overlay with bounding boxes showing detected text locations
- **Structured Output**: Comprehensive JSON results including:
  - Extracted text with confidence levels
  - Bounding box coordinates
  - Processing metadata (language, DPI, settings used)
- **Data Export**: Download structured data as JSON files
- **Real-time Preview**: Live preview of processed images with OCR overlay

### API and Integration
- **REST API Endpoints**: Simple programmatic access via `/api/v1/` endpoints:
  - `/ocr` - File processing endpoint
  - `/formats` - Get supported file formats
  - `/languages` - List available OCR languages
  - `/health` - Service health check
  - `/docs` - API documentation
- **API Testing**: Built-in API testing interface for easy endpoint testing
- **Simple Integration**: No authentication required for prototype usage

---

## 🎯 Development Guidelines

### Critical Success Factors for the Prototype
1. **Simplicity**: Avoid over-engineering. The goal is a functional proof-of-concept, not a production system.
2. **Local First**: All functionality must work offline on a local Windows machine. No external APIs or services.
3. **Follow the Plan**: Stick to the features and steps outlined in the `Implementation Plan_ Docusense Prototype.md`.

### Development Workflow
1.  **Implement a feature** as described in the plan (e.g., add the `process_image` function).
2.  **Run the Flask server**: `python app.py`.
3.  **Manually test** the new functionality in the browser.
4.  Repeat until all phases of the implementation plan are complete.

---

## 🔧 Development Environment

### Local Setup Requirements
- **OS**: Windows 10/11
- **Python**: 3.9+
- **Tesseract OCR**: UB-Mannheim build installed and added to PATH.
- **Poppler**: Windows binaries downloaded and `bin` folder added to PATH.

### Quick Start Commands
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the application
python app.py
```

### Health Check
- **Primary Check**: Open `http://127.0.0.1:5000` in a web browser. The interface should load without errors.
- **Functionality Check**: Upload a test document and verify that you receive an output.

---

## 🔐 Security Guidelines

This is a local-only prototype and is **not intended for production use**. It has not been hardened for security.
- Do not expose the application to the internet.
- The file upload mechanism is basic and does not include security checks against malicious files.
- The file serving endpoint allows access to any file in the `uploads` directory without authentication.

---

## 📚 Documentation Structure

### Essential Documentation Files
- `README.md` - Project overview and quick start.
- `Implementation Plan_ Docusense Prototype.md` - The primary source of truth for the project tasks.
- `docs/Project_Master_Context.md` - Project architecture and context (this file).
- `docs/Project_TODO_List.md` - Development priorities and status.
- `docs/STARTUP_GUIDE.md` - System startup and configuration.
- `docs/Testing_Guide.md` - Manual testing procedures.
- `docs/Development_Guide.md` - Development practices.