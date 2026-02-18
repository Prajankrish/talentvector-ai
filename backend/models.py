"""
Pydantic models for TalentVector AI
Defines data structures for candidates, jobs, and evaluations.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Skill(BaseModel):
    """Represents a skill"""
    name: str
    level: str  # beginner, intermediate, advanced, expert
    years_experience: Optional[int] = None

class Experience(BaseModel):
    """Represents work experience"""
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None

class Education(BaseModel):
    """Represents education"""
    institution: str
    degree: str
    field: str
    graduation_date: Optional[str] = None

class Candidate(BaseModel):
    """Candidate model"""
    id: Optional[str] = None
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: List[Skill] = []
    experience: List[Experience] = []
    education: List[Education] = []
    resume_text: Optional[str] = None
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class JobPosition(BaseModel):
    """Job position model"""
    id: Optional[str] = None
    title: str
    description: str
    required_skills: List[str] = []
    required_experience: int  # years
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None

class ScreeningResult(BaseModel):
    """Resume screening result"""
    candidate_id: str
    job_id: str
    score: float  # 0-100
    recommendation: str  # approved, rejected, review
    reasoning: str
    created_at: Optional[datetime] = None

class MatchResult(BaseModel):
    """Candidate-job match result"""
    candidate_id: str
    job_id: str
    similarity_score: float  # 0-1
    match_percentage: float  # 0-100
    reasoning: str
