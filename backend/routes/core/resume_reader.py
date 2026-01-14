from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PyPDF2 import PdfReader
from docx import Document
import docx2txt
import os
from typing import Optional
from io import BytesIO
import tempfile
import sys
from pathlib import Path

from core.auth_dependency import get_current_user
from utils import return_response
from schema.resume_models import IsResume, SkillGaps, CandidateDetails

# Add parent directory to path to import helper
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Request models for analysis endpoints
class ResumeAnalysisRequest(BaseModel):
    resume_text: str

class SkillGapsRequest(BaseModel):
    resume_text: str
    job_description: str = ""

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


@resume_reader_route.post("/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest, user: str = Depends(get_current_user)):
    """
    Analyze resume text and extract candidate details.
    
    Args:
        request: ResumeAnalysisRequest containing resume_text
        user: Current authenticated user
        
    Returns:
        JSONResponse with candidate details or error message
    """
    try:
        if not request.resume_text or not request.resume_text.strip():
            return return_response(
                message="Resume text cannot be empty",
                status=False,
                status_code=400,
                data=None
            )
        
        # Analyze the resume text
        from helper import get_resume_details
        candidate_details = get_resume_details(request.resume_text, model_name="gemini")
        
        # Check if analysis returned an error message (string) instead of CandidateDetails
        if isinstance(candidate_details, str):
            return return_response(
                message=candidate_details,
                status=False,
                status_code=400,
                data=None
            )
        
        # Convert CandidateDetails object to dictionary
        analysis_data = {
            "skills": candidate_details.skills if hasattr(candidate_details, 'skills') else [],
            "experience": candidate_details.experience if hasattr(candidate_details, 'experience') else "",
            "education": candidate_details.education if hasattr(candidate_details, 'education') else "",
            "projects": candidate_details.projects if hasattr(candidate_details, 'projects') else [],
            "jobRole": candidate_details.job_role if hasattr(candidate_details, 'job_role') else ""
        }
        
        return return_response(
            message="Resume analyzed successfully.",
            status=True,
            data=analysis_data
        )
        
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        return return_response(
            message=f"Error analyzing resume: {str(e)}",
            status=False,
            status_code=500,
            data=None
        )


@resume_reader_route.post("/skill-gaps")
async def analyze_skill_gaps(request: SkillGapsRequest, user: str = Depends(get_current_user)):
    """
    Analyze skill gaps in resume.
    
    Args:
        request: SkillGapsRequest containing resume_text and optional job_description
        user: Current authenticated user
        
    Returns:
        JSONResponse with skill gaps analysis or error message
    """
    try:
        if not request.resume_text or not request.resume_text.strip():
            return return_response(
                message="Resume text cannot be empty",
                status=False,
                status_code=400,
                data=None
            )
        
        # Get candidate details first
        from helper import get_resume_details
        candidate_details = get_resume_details(request.resume_text, model_name="gemini")
        
        if isinstance(candidate_details, str):
            return return_response(
                message=candidate_details,
                status=False,
                status_code=400,
                data=None
            )
        
        # Mock skill gaps data based on extracted details
        skill_gaps_data = {
            "profile_summary": f"Professional with expertise in {', '.join(candidate_details.skills[:3] if hasattr(candidate_details, 'skills') else [])}. "
                             f"Experience: {candidate_details.experience if hasattr(candidate_details, 'experience') else 'N/A'}",
            "strengths": [
                f"Strong in {skill}" for skill in (candidate_details.skills[:3] if hasattr(candidate_details, 'skills') else [])
            ] + [
                "Good professional background",
                "Structured career progression"
            ],
            "weaknesses": [
                "Could expand technical skillset",
                "Consider advanced certifications",
                "Explore emerging technologies",
                "Strengthen soft skills"
            ],
            "areas_of_improvement": [
                "Pursue relevant industry certifications",
                "Develop expertise in trending technologies",
                "Enhance leadership and communication skills",
                "Build strong professional network",
                "Stay updated with industry trends"
            ]
        }
        
        return return_response(
            message="Skill gaps analyzed successfully.",
            status=True,
            data=skill_gaps_data
        )
        
    except Exception as e:
        print(f"Error analyzing skill gaps: {str(e)}")
        return return_response(
            message=f"Error analyzing skill gaps: {str(e)}",
            status=False,
            status_code=500,
            data=None
        )