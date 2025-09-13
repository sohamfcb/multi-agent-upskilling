from pydantic import BaseModel, Field
from typing import Optional, Literal

class CandidateDetails(BaseModel):
    """
    Pydantic model for storing candidate details extracted from resume.
    
    Attributes:
        skills (str): All skills of the candidate
        experience (str): Years of experience
        education (str): Education details (degree, stream, college)
        projects (List[str]): List of project summaries
        job_role (str): Recommended job role(s)
        location (Optional[str]): Candidate's location if mentioned
    """
    skills: str = Field(description="Extract all the skills of the candidate from the resume")
    experience: str = Field(description="Extract the number of years of experience of the candidate from the resume")
    education: str = Field(description="Extract the education details (like degree, stream, college, etc.) of the candidate from the resume")
    projects: list[str] = Field(description="Extract all the projects and put it inside a list. It should only contain a one liner gist of the project.")
    job_role: str = Field(description="Extract one or more job roles for the candidate according to the resume")
    location: Optional[str] = Field(description="Extract the location of the candidate if mentioned in the resume.")

class IsResume(BaseModel):
    """
    Pydantic model for validating if a document is a resume.
    
    Attributes:
        is_resume (Literal["yes", "no"]): Whether the document is a resume
    """
    is_resume: Literal["yes", "no"] = Field(description="Determine if the given text is a resume or not. If it is a resume, return \"yes\", else return \"no\"")

class SkillGaps(BaseModel):
    """
    Pydantic model for storing skill gap analysis results.
    
    Attributes:
        profile_summary (str): Summary of candidate's profile
        strengths (List[str]): List of candidate's strengths
        weaknesses (List[str]): List of candidate's weaknesses and skill gaps
        areas_of_improvement (List[str]): Areas where candidate can improve
    """
    profile_summary: str = Field(description="Extract the profile summary like skills, projects, education, experience")
    strengths: list[str] = Field(description="Extract all the strenghts of the candidate.")
    weaknesses: list[str] = Field(description="Extract the weaknesses and skill gaps of the candidate.")
    areas_of_improvement: list[str] = Field(description="Extract the areas of improvement for the candidate in question.")