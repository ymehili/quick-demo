from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os
import io
import magic
from typing import Optional

app = FastAPI(title="OCR + PDF Generation Demo", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "FastAPI OCR + PDF Generation Demo"}

@app.post("/ocr/")
async def extract_text_from_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        extracted_text = pytesseract.image_to_string(image)
        
        return {
            "filename": file.filename,
            "extracted_text": extracted_text,
            "text_length": len(extracted_text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/generate-pdf/")
async def generate_pdf(
    text: str = Form(...),
    title: Optional[str] = Form("Generated Document")
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            doc = SimpleDocTemplate(tmp_file.name, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            title_paragraph = Paragraph(title, styles['Title'])
            story.append(title_paragraph)
            story.append(Spacer(1, 12))
            
            text_paragraph = Paragraph(text, styles['Normal'])
            story.append(text_paragraph)
            
            doc.build(story)
            
            return FileResponse(
                tmp_file.name,
                media_type="application/pdf",
                filename="generated_document.pdf"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.post("/ocr-to-pdf/")
async def ocr_to_pdf(
    file: UploadFile = File(...),
    title: Optional[str] = Form("OCR Document")
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        extracted_text = pytesseract.image_to_string(image)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            doc = SimpleDocTemplate(tmp_file.name, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            title_paragraph = Paragraph(title, styles['Title'])
            story.append(title_paragraph)
            story.append(Spacer(1, 12))
            
            source_info = Paragraph(f"Extracted from: {file.filename}", styles['Italic'])
            story.append(source_info)
            story.append(Spacer(1, 12))
            
            text_paragraph = Paragraph(extracted_text, styles['Normal'])
            story.append(text_paragraph)
            
            doc.build(story)
            
            return FileResponse(
                tmp_file.name,
                media_type="application/pdf",
                filename=f"ocr_{file.filename.split('.')[0]}.pdf"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image to PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)