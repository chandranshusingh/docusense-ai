# Testing Guide - Docusense OCR Prototype

**Document Purpose**: A guide for manually testing the OCR prototype.
**Version**: 0.1.0 (Prototype)
**Status**: ✅ **ACTIVE TESTING** - Manual testing procedures are defined.

---

## 🧪 **TESTING OVERVIEW**

For this prototype, all testing is performed **manually**. The goal is to ensure the core functionality works as expected across the supported file types. There is no automated test suite.

### **Testing Success Criteria**
- The application starts without errors.
- The web interface loads and is usable.
- All supported file types (6 core formats) are processed correctly.
- Advanced OCR settings (DPI, language, engine parameters) function properly.
- REST API endpoints respond correctly without authentication requirements.
- Enhanced PDF processing works for multi-page documents.
- Spreadsheet processing extracts data correctly from CSV and Excel files.
- The output (image preview, bounding boxes, text, JSON) is accurate.
- The application handles error cases gracefully across all features.

---

## 🚀 **HOW TO TEST**

### **1. Pre-Testing Setup**
1.  Make sure the application is running (`python app.py`).
2.  Open your web browser and navigate to `http://127.0.0.1:5000`.
3.  Prepare a comprehensive set of test files, including at least one of each supported type:
    - **Images**: `.png`, `.jpg`, `.jpeg` with clear text
    - **Documents**: `.pdf` (both selectable and scanned text, including multi-page), `.docx`, `.txt`
    - **Spreadsheets**: `.csv`, `.xls`, `.xlsx` with text content
    - **Unsupported files**: `.zip`, `.mp3`, `.exe` for error handling tests
4.  Have different language sample files ready (if testing multi-language OCR).
5.  Prepare API testing tools: Postman, curl, or similar HTTP clients.
6.  Prepare multi-page PDF files to test enhanced PDF processing.

---

## 📊 **MANUAL TEST CASES**

Execute the following test cases to verify the application's functionality.

### **Test Case 1: Image File (Happy Path)**
1.  **Action**: Upload a `.png` or `.jpg` file with text.
2.  **Expected Result**:
    - The "Results" section becomes visible.
    - A preview of the uploaded image is displayed.
    - A canvas with semi-transparent red boxes is drawn over the detected text on the image.
    - The "Plain Text" `textarea` is populated with the text extracted from the image.
    - The "Structured JSON" `textarea` contains detailed data, including text, confidence, and bounding box coordinates.
    - The "Download JSON" button works and downloads a valid `.json` file.

### **Test Case 2: PDF File (Happy Path)**
1.  **Action**: Upload a `.pdf` file.
2.  **Expected Result**:
    - The "Results" section appears.
    - A preview image *of the first page of the PDF* is displayed.
    - Red bounding boxes are drawn over the detected text in the preview image.
    - The textareas are populated with the extracted text and structured data from the first page.
    - The JSON download works correctly.

### **Test Case 3: DOCX File (Text Extraction)**
1.  **Action**: Upload a `.docx` file.
2.  **Expected Result**:
    - The "Results" section appears.
    - The image preview area is hidden or empty.
    - The "Plain Text" `textarea` is populated with the full text content from the document.
    - The "Structured JSON" `textarea` contains a simple object with the extracted text (e.g., `{"text_only": "..."}`).
    - The JSON download works.

### **Test Case 4: TXT File (Text Extraction)**
1.  **Action**: Upload a `.txt` file.
2.  **Expected Result**:
    - The "Results" section appears.
    - The image preview area is hidden or empty.
    - The "Plain Text" `textarea` shows the exact content of the `.txt` file.
    - The "Structured JSON" `textarea` contains a simple object with the extracted text.
    - The JSON download works.

### **Test Case 5: Unsupported File Type (Error Handling)**
1.  **Action**: Attempt to upload a file with an unsupported extension (e.g., `.zip`, `.exe`).
2.  **Expected Result**:
    - The upload is rejected by the frontend or backend.
    - An error message is displayed to the user indicating the file type is not allowed.
    - No results are displayed.

### **Test Case 6: No File Selected (Error Handling)**
1.  **Action**: Click the "Upload" button without selecting a file.
2.  **Expected Result**:
    - The form does not submit.
    - An error message is displayed, prompting the user to select a file first.

---

## 📊 **EXTENDED FEATURE TEST CASES**

### **Test Case 7: Enhanced PDF Processing (Multi-page)**
1.  **Action**: Upload multi-page PDF files with both text-based and image-based content.
2.  **Expected Result**:
    - All pages are processed, not just the first page.
    - Text-based PDFs have text directly extracted without OCR.
    - Image-based PDFs use OCR processing for text extraction.
    - Results include page information in the JSON structure.
    - Both types of PDFs display properly in the interface.
    - Consolidated results from all pages are provided.

### **Test Case 8: Spreadsheet File Processing (CSV, Excel)**
1.  **Action**: Upload `.csv`, `.xls`, and `.xlsx` files with data.
2.  **Expected Result**:
    - All spreadsheet formats are processed successfully.
    - Cell content is extracted and formatted as structured text.
    - Table structure is preserved in plain text output.
    - Empty cells and merged cells are handled appropriately.
    - Multi-sheet Excel files process all sheets.

### **Test Case 10: DPI Configuration Testing**
1.  **Action**: Upload the same image with different DPI settings (150, 300, 600).
2.  **Expected Result**:
    - DPI selection dropdown functions correctly.
    - Different DPI settings produce varying OCR accuracy results.
    - Processing time varies appropriately with DPI.
    - DPI information is included in the JSON response.
    - Image preprocessing works correctly for each DPI setting.

### **Test Case 11: Multi-Language OCR Testing**
1.  **Action**: Upload images containing text in different languages (English, French, German, Spanish).
2.  **Expected Result**:
    - Language selection dropdown shows available language packs.
    - OCR accuracy improves when correct language is selected.
    - Language information is included in JSON response.
    - Error messages appear for missing language packs.
    - Combined language processing works when available.

### **Test Case 12: Advanced OCR Parameters Testing**
1.  **Action**: Test different OCR engine modes and page segmentation settings.
2.  **Expected Result**:
    - Advanced settings panel functions correctly.
    - Different engine modes (Legacy, LSTM, Combined) produce varying results.
    - Page segmentation modes work appropriately for different document types.
    - Character whitelist/blacklist filters function correctly.
    - Tooltips and help text provide useful guidance.

---

## 🌐 **API ENDPOINT TEST CASES**

### **Test Case 13: Core API Endpoints**
1.  **Action**: Test `POST /api/v1/ocr` endpoint with file upload via HTTP client.
2.  **Expected Result**:
    - Endpoint accepts multipart/form-data file uploads without authentication.
    - Returns proper JSON response with OCR results.
    - HTTP status codes are correct (200 for success, 400/422 for errors).
    - Response format matches web interface results.
    - All supported file formats work through API.

### **Test Case 14: API Information Endpoints**
1.  **Action**: Test `GET /api/v1/formats`, `GET /api/v1/languages`, and `GET /api/v1/health`.
2.  **Expected Result**:
    - `/formats` returns list of supported file extensions.
    - `/languages` returns available Tesseract language packs.
    - `/health` returns basic service status and version information.
    - All responses use consistent JSON format.
    - HTTP status codes are appropriate.
    - No authentication required for any endpoint.

### **Test Case 15: API Documentation and Testing Interface**
1.  **Action**: Access `GET /api/v1/docs` and `/api-test` endpoints.
2.  **Expected Result**:
    - Documentation endpoint returns basic API reference with request/response examples.
    - API testing interface provides forms for all endpoints.
    - Usage examples are accurate and helpful for each endpoint.
    - Testing page demonstrates API usage without authentication requirements.
    - All endpoints are accessible and functional through the testing interface.

---

## 🔍 **ERROR HANDLING AND EDGE CASES**

### **Test Case 18: File Size and Format Limits**
1.  **Action**: Upload extremely large files and various corrupted files.
2.  **Expected Result**:
    - Large files are handled gracefully with appropriate timeouts.
    - Corrupted files return meaningful error messages.
    - File size limits are enforced if configured.
    - Memory usage remains reasonable during processing.
    - Server doesn't crash with malformed files.

### **Test Case 19: Concurrent Processing**
1.  **Action**: Submit multiple files simultaneously through web interface and API.
2.  **Expected Result**:
    - Multiple uploads are handled correctly.
    - No file mixing or corruption occurs.
    - Response times remain reasonable under load.
    - Server resources are managed appropriately.
    - Error handling works under concurrent load.

### **Test Case 20: Configuration Edge Cases**
1.  **Action**: Test extreme OCR settings and missing dependencies.
2.  **Expected Result**:
    - Very high DPI settings work or fail gracefully.
    - Missing language packs are detected and reported.
    - Invalid OCR parameters are rejected with helpful messages.
    - Default settings are used when custom settings fail.
    - Configuration validation prevents system crashes.

---

## 📁 **TESTING STRUCTURE**

```
testing/
├── scripts/              # Test execution scripts
│   ├── test_runner.py    # Main test runner
│   ├── test_integration_simple.py
│   ├── test_performance.py
│   └── test_api.py
├── unit/                 # Unit tests
│   ├── test_api.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/          # Integration tests
│   ├── test_endpoints.py
│   └── test_services.py
├── performance/          # Performance tests
│   ├── test_load.py
│   └── test_stress.py
├── e2e/                 # End-to-end tests
│   ├── test_user_journeys.py
│   └── test_workflows.py
├── reports/             # Test reports
│   ├── test_summary.txt
│   ├── performance_report.json
│   └── coverage_report.html
└── fixtures/            # Test data and fixtures
    ├── test_data.json
    └── mock_responses.json
```

---

## 🔧 **TESTING WORKFLOW**

### **1. Pre-Testing Setup**
```powershell
# 1. Ensure you're in project root
cd D:\Your\Project\Path

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Start services
.\start_project.ps1

# 4. Wait for services to be ready
Start-Sleep -Seconds 10
```

### **2. Running Tests**

#### **Complete Test Suite**
```powershell
# Run all tests
python testing/scripts/test_runner.py

# Check results
Get-Content testing/reports/test_summary.txt
```

#### **Specific Test Categories**
```powershell
# Unit tests only
python -m pytest testing/unit/ -v

# Integration tests
python testing/scripts/test_integration_simple.py

# Performance tests
python testing/scripts/test_performance.py

# API tests
python testing/scripts/test_api.py
```

#### **Individual Test Files**
```powershell
# Specific test file
python -m pytest testing/unit/test_api.py -v

# Specific test function
python -m pytest testing/unit/test_api.py::test_endpoint_response -v
```

### **3. Test Results Analysis**

#### **Success Rate Monitoring**
```powershell
# Check test success rate
$results = Get-Content testing/reports/test_summary.txt
$successRate = ($results | Select-String "PASSED").Count / ($results | Select-String "PASSED|FAILED").Count * 100
Write-Host "Test Success Rate: $successRate%"
```

#### **Performance Monitoring**
```powershell
# Check response times
$response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
$responseTime = $response.BaseResponse.ResponseTime
Write-Host "Response Time: $responseTime ms"
```

---

## 📊 **TEST CATEGORIES**

### **1. Unit Tests**

#### **Purpose**
- Test individual functions and methods
- Verify component behavior in isolation
- Ensure code quality and reliability

#### **Example Unit Test**
```python
import pytest
from src.api.endpoints import process_data

def test_process_data_valid_input():
    """Test data processing with valid input."""
    input_data = {"key": "value"}
    result = process_data(input_data)
    
    assert result is not None
    assert "processed" in result
    assert result["status"] == "success"

def test_process_data_invalid_input():
    """Test data processing with invalid input."""
    with pytest.raises(ValueError):
        process_data(None)
```

#### **Running Unit Tests**
```powershell
# All unit tests
python -m pytest testing/unit/ -v

# Specific unit test file
python -m pytest testing/unit/test_api.py -v

# With coverage
python -m pytest testing/unit/ --cov=src --cov-report=html
```

### **2. Integration Tests**

#### **Purpose**
- Test component interactions
- Verify API endpoint functionality
- Ensure service integration

#### **Example Integration Test**
```python
import pytest
import requests

def test_api_endpoint_integration():
    """Test API endpoint integration."""
    url = "http://localhost:8000/api/endpoint"
    data = {"test": "data"}
    
    response = requests.post(url, json=data)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_service_integration():
    """Test service integration."""
    # Test service communication
    pass
```

#### **Running Integration Tests**
```powershell
# Integration tests
python testing/scripts/test_integration_simple.py

# Specific integration test
python -m pytest testing/integration/test_endpoints.py -v
```

### **3. API Tests**

#### **Purpose**
- Validate REST API endpoints
- Test request/response formats
- Verify error handling

#### **Example API Test**
```python
import pytest
import requests

class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_health_endpoint(self):
        """Test health endpoint."""
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_api_endpoint_post(self):
        """Test API endpoint POST method."""
        url = "http://localhost:8000/api/endpoint"
        data = {"test": "data"}
        
        response = requests.post(url, json=data)
        assert response.status_code == 200
        
        result = response.json()
        assert "status" in result
        assert result["status"] == "success"
    
    def test_api_endpoint_invalid_data(self):
        """Test API endpoint with invalid data."""
        url = "http://localhost:8000/api/endpoint"
        data = {"invalid": "data"}
        
        response = requests.post(url, json=data)
        assert response.status_code == 422
```

#### **Running API Tests**
```powershell
# API tests
python testing/scripts/test_api.py

# Specific API test
python -m pytest testing/unit/test_api.py::TestAPIEndpoints -v
```

### **4. Performance Tests**

#### **Purpose**
- Measure response times
- Test system under load
- Verify performance benchmarks

#### **Example Performance Test**
```python
import time
import requests
import statistics

def test_response_time():
    """Test API response time."""
    url = "http://localhost:8000/api/endpoint"
    data = {"test": "data"}
    
    times = []
    for _ in range(10):
        start_time = time.time()
        response = requests.post(url, json=data)
        end_time = time.time()
        
        assert response.status_code == 200
        times.append(end_time - start_time)
    
    avg_time = statistics.mean(times)
    assert avg_time < 2.0  # Less than 2 seconds

def test_load_performance():
    """Test system under load."""
    url = "http://localhost:8000/api/endpoint"
    data = {"test": "data"}
    
    # Simulate concurrent requests
    import concurrent.futures
    
    def make_request():
        return requests.post(url, json=data)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        responses = [future.result() for future in futures]
    
    success_count = sum(1 for r in responses if r.status_code == 200)
    assert success_count >= 45  # 90% success rate
```

#### **Running Performance Tests**
```powershell
# Performance tests
python testing/scripts/test_performance.py

# Load testing
python testing/scripts/test_load_performance.py
```

### **5. Frontend Tests**

#### **Purpose**
- Test UI components
- Verify accessibility
- Test user interactions

#### **Example Frontend Test**
```javascript
// Frontend test example (if using Selenium or similar)
describe('Frontend Tests', () => {
    test('should load main page', async () => {
        const response = await fetch('http://localhost:3000/');
        expect(response.status).toBe(200);
    });
    
    test('should have accessible elements', () => {
        // Test accessibility features
        const mainContent = document.querySelector('main');
        expect(mainContent).toBeTruthy();
    });
});
```

#### **Running Frontend Tests**
```powershell
# Frontend tests (if implemented)
python testing/scripts/test_frontend.py
```

### **6. E2E Tests**

#### **Purpose**
- Test complete user journeys
- Verify end-to-end workflows
- Test real user scenarios

#### **Example E2E Test**
```python
import pytest
import requests

def test_complete_user_journey():
    """Test complete user journey."""
    # 1. Start session
    session_response = requests.post("http://localhost:8000/api/session")
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # 2. Send data
    data_response = requests.post(
        f"http://localhost:8000/api/endpoint",
        json={"session_id": session_id, "data": "test"}
    )
    assert data_response.status_code == 200
    
    # 3. Get results
    results_response = requests.get(
        f"http://localhost:8000/api/results/{session_id}"
    )
    assert results_response.status_code == 200
    
    # 4. Verify final state
    final_response = requests.get(
        f"http://localhost:8000/api/status/{session_id}"
    )
    assert final_response.status_code == 200
    assert final_response.json()["status"] == "completed"
```

#### **Running E2E Tests**
```powershell
# E2E tests
python testing/scripts/test_e2e.py

# Specific E2E test
python -m pytest testing/e2e/test_user_journeys.py -v
```

---

## 📈 **PERFORMANCE TESTING**

### **Response Time Testing**
```powershell
# Test response time
$start = Get-Date
$response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
$end = Get-Date
$duration = ($end - $start).TotalMilliseconds
Write-Host "Response Time: $duration ms"

# Verify performance target
if ($duration -lt 2000) {
    Write-Host "✅ Performance target met (<2s)"
} else {
    Write-Host "❌ Performance target exceeded"
}
```

### **Load Testing**
```powershell
# Simple load test
$url = "http://localhost:8000/api/endpoint"
$data = @{test="data"} | ConvertTo-Json

$jobs = @()
for ($i = 1; $i -le 10; $i++) {
    $job = Start-Job -ScriptBlock {
        param($url, $data)
        try {
            $response = Invoke-WebRequest -Uri $url -Method POST -Body $data -ContentType "application/json"
            return $response.StatusCode
        } catch {
            return $_.Exception.Response.StatusCode
        }
    } -ArgumentList $url, $data
    $jobs += $job
}

$results = $jobs | Wait-Job | Receive-Job
$successCount = ($results | Where-Object { $_ -eq 200 }).Count
$successRate = ($successCount / $results.Count) * 100

Write-Host "Load Test Results: $successRate% success rate"
```

---

## 🚨 **TROUBLESHOOTING TESTS**

### **Common Test Issues**

#### **1. Import Errors**
```powershell
# Problem: ModuleNotFoundError
# Solution: Run from project root
cd D:\Your\Project\Path
python testing/scripts/test_runner.py
```

#### **2. Service Not Available**
```powershell
# Problem: Connection refused
# Solution: Start services first
.\start_project.ps1
Start-Sleep -Seconds 10
python testing/scripts/test_runner.py
```

#### **3. Port Conflicts**
```powershell
# Problem: Port already in use
# Solution: Check and kill processes
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

#### **4. Test Timeouts**
```powershell
# Problem: Tests hanging
# Solution: Add timeout to test runner
$job = Start-Job -ScriptBlock { python testing/scripts/test_runner.py }
$result = Wait-Job -Job $job -Timeout 300  # 5 minute timeout
if ($result) {
    $output = Receive-Job -Job $job
    Write-Host $output
} else {
    Write-Host "Test timed out"
}
```

### **Debugging Test Failures**

#### **Enable Debug Logging**
```powershell
# Enable debug mode
$env:LOG_LEVEL = "DEBUG"
python testing/scripts/test_runner.py
```

#### **Check Test Logs**
```powershell
# View test logs
Get-Content testing/reports/test_summary.txt

# View detailed logs
Get-Content logs\testing\test_runner.log -Tail 50
```

#### **Manual Testing**
```powershell
# Test specific endpoint manually
curl -X POST http://localhost:8000/api/endpoint -H "Content-Type: application/json" -d "{\"test\":\"data\"}"

# Check service health
curl http://localhost:8000/health
```

---

## 📊 **TEST REPORTING**

### **Test Summary Report**
```powershell
# Generate test summary
python testing/scripts/generate_test_report.py

# View summary
Get-Content testing/reports/test_summary.txt
```

### **Performance Report**
```powershell
# Generate performance report
python testing/scripts/generate_performance_report.py

# View performance metrics
Get-Content testing/reports/performance_report.json | ConvertFrom-Json
```

### **Coverage Report**
```powershell
# Generate coverage report
python -m pytest testing/unit/ --cov=src --cov-report=html

# View coverage report
Start-Process testing/reports/htmlcov/index.html
```

---

## 🎯 **TEST QUALITY STANDARDS**

### **Success Criteria**
- **Test Success Rate**: 90%+ across all categories
- **Response Time**: <2 seconds for all operations
- **Code Coverage**: 90%+ coverage target
- **Performance**: Meet all performance benchmarks
- **Reliability**: Tests run consistently without flakiness

### **Quality Checklist**
- [ ] All tests pass consistently
- [ ] Response times meet targets
- [ ] Code coverage meets requirements
- [ ] Performance benchmarks achieved
- [ ] Error handling tested
- [ ] Edge cases covered
- [ ] Documentation updated
- [ ] Test data properly managed

---

## 📚 **TESTING RESOURCES**

### **Documentation**
- **Project Master Context**: `docs/Project_Master_Context.md`
- **Development Guide**: `docs/Development_Guide.md`
- **API Documentation**: `http://localhost:8000/docs`

### **External Resources**
- **Pytest Documentation**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **Python Testing**: https://docs.python.org/3/library/unittest.html

---

**This testing guide provides comprehensive coverage of the testing framework and should be updated as the system evolves.**