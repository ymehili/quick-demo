# FastAPI OCR + PDF Generation Demo

A simple FastAPI application that demonstrates OCR (Optical Character Recognition) and PDF generation capabilities.

## Features

- **OCR Endpoint**: Extract text from uploaded images using Tesseract
- **PDF Generation**: Create PDF documents from text input
- **Combined OCR-to-PDF**: Extract text from images and generate PDFs in one step
- **Web Interface**: Simple HTML frontend for testing all features

## Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system

### Installing Tesseract

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. OCR Text Extraction
- **POST** `/ocr/`
- Upload an image file to extract text
- Returns JSON with extracted text

### 2. PDF Generation
- **POST** `/generate-pdf/`
- Generate PDF from text input
- Form data: `text` (required), `title` (optional)

### 3. OCR to PDF
- **POST** `/ocr-to-pdf/`
- Extract text from image and generate PDF
- Form data: `file` (image), `title` (optional)

## Testing

1. Start the server: `python main.py`
2. Open `demo.html` in your browser
3. Test each feature with sample images

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.