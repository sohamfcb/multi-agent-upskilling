from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from docx import Document
import docx2txt
import os
from typing import Optional
from io import BytesIO
import tempfile

from core.auth_dependency import get_current_user
from utils import return_response

from schema.resume_models import IsResume, SkillGaps, CandidateDetails

# helper that accepts bytes or a file path
def extract_text_from_bytes(file_bytes: bytes, filename: str) -> Optional[str]:
    """
    Accepts raw bytes and filename; returns extracted text or None.
    Supports: .pdf, .docx, .doc
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        try:
            reader = PdfReader(BytesIO(file_bytes))
            pages = []
            for p in reader.pages:
                t = p.extract_text()
                if t:
                    pages.append(t)
            return "\n".join(pages).strip()
        except Exception as e:
            print("PDF extraction error:", e)
            return None

    elif ext in [".docx", ".doc"]:
        # Try python-docx using a temp file (python-docx expects a path or file-like object)
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tf:
                tf.write(file_bytes)
                tmp_path = tf.name

            # Try python-docx first
            text_parts = []
            try:
                doc = Document(tmp_path)
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                text_parts.extend(paragraphs)

                # extract table text
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            if cell.text.strip():
                                text_parts.append(cell.text.strip())
            except Exception as e:
                # python-docx might fail on some .doc/.docx files; we'll fallback to docx2txt
                print("python-docx failed:", e)

            text = "\n".join(text_parts).strip()
            if not text:
                # fallback to docx2txt
                try:
                    text = docx2txt.process(tmp_path).strip()
                except Exception as e:
                    print("docx2txt failed:", e)
                    text = ""

            return text if text else None

        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    else:
        # unknown extension — return None (you can add image OCR handling here)
        return None

resume_reader_route=APIRouter(prefix="/core")

@resume_reader_route.post("/read-resume")
async def read_resume(resume: UploadFile, user: str = Depends(get_current_user)):
    """
    Accepts a single file upload (UploadFile). Reads bytes, extracts text, returns JSON.
    """
    # basic validation — optional
    filename = resume.filename or "uploaded_file"
    ext = os.path.splitext(filename)[1].lower()
    allowed = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    # read bytes from UploadFile — THIS IS ASYNC
    file_bytes = await resume.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # If it's an image and you have an OCR helper, call it here.
    # For now we'll only handle pdf/docx/doc
    if ext in {".pdf", ".docx", ".doc"}:
        text = extract_text_from_bytes(file_bytes, filename)
    else:
        # If you want vision OCR for images, call your image OCR function here:
        # text = get_resume_details_from_image(temp_image_path) or similar
        text = None

    if text is None:
        return return_response(message="Could bot extract text.", status=False, status_code=400, data=None)

    return return_response(message="Resume uploaded successfully.", status=True, data=text)


# @resume_reader_route.post("/parse-resume", r)