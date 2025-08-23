# schemas/user_profile.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class UserProfileIn(BaseModel):
    user_id: UUID
    highest_qualification: Optional[str] = Field(None, max_length=120)
    degree: Optional[str] = Field(None, max_length=120)
    institution: Optional[str] = Field(None, max_length=120)
    graduation_year: Optional[int] = None
    years_experience: Optional[int] = None
    current_job_title: Optional[str] = Field(None, max_length=120)
    current_company: Optional[str] = Field(None, max_length=120)
    skills: Optional[List[str]] = None        # maps to TEXT[] in PG
    career_goal_short: Optional[str] = None
    career_goal_long: Optional[str] = None
    resume_url: Optional[str] = None

class UserProfileOut(UserProfileIn):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
