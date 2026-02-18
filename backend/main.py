"""
TalentVector AI - FastAPI Backend
REST API for resume parsing, screening, and candidate matching.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

# Import backend modules
from utils import setup_logger, Config, APIError
from hiring_manager import HiringManager
from resume_parser import ResumeParser
from screening import CandidateScreener
from matching import CandidateJobMatcher
from feedback import FeedbackCollector

# Setup logging
logger = setup_logger(__name__)

# Validate configuration
is_valid, errors = Config.validate()
if not is_valid:
    logger.error(f"Configuration validation failed: {errors}")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="TalentVector AI API",
    description="AI-native recruiting system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize backend modules
try:
    hiring_manager = HiringManager()
    resume_parser = ResumeParser()
    screener = CandidateScreener()
    matcher = CandidateJobMatcher()
    feedback_collector = FeedbackCollector()
    logger.info("✅ All backup modules initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize modules: {str(e)}")
    # Don't exit, let the endpoints return error responses


# ===== Pydantic Models =====

class HiringProfileRequest(BaseModel):
    """Request model for hiring profile creation"""
    role_title: str
    required_skills: List[str]
    nice_to_have_skills: Optional[List[str]] = []
    years_of_experience: int
    industry: str
    team_culture_description: str
    job_level: Optional[str] = None
    salary_range: Optional[str] = None
    qualifications: Optional[str] = None


class ResumeParsingRequest(BaseModel):
    """Request model for resume parsing"""
    resume_text: str


class ScreeningRequest(BaseModel):
    """Request model for screening questions"""
    hiring_profile: dict
    num_questions: int = 4


class MatchingRequest(BaseModel):
    """Request model for candidate-job matching"""
    candidate_profile: dict
    hiring_profile: dict
    screening_score: float = 7.0


class FeedbackRequest(BaseModel):
    """Request model for feedback recording"""
    candidate_id: str
    hiring_manager_id: str
    final_score: float
    feedback: str
    notes: Optional[str] = None


class ScreeningEvaluationRequest(BaseModel):
    """Request model for screening evaluation"""
    hiring_profile: dict
    questions: List[dict]
    answers: dict


# ===== Health Check Endpoints =====

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TalentVector AI API",
        "version": "1.0.0",
        "model": Config.GEMINI_MODEL
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "database": "ready",
        "llm": "available",
        "gemini_model": Config.GEMINI_MODEL,
        "api_host": Config.API_HOST,
        "api_port": Config.API_PORT
    }


# ===== Hiring Manager Endpoints =====

@app.post("/api/hiring-profile")
async def create_hiring_profile(request: HiringProfileRequest):
    """Create a structured hiring profile"""
    try:
        logger.info(f"Creating hiring profile for role: {request.role_title}")
        
        result = hiring_manager.process_hiring_input(
            role_title=request.role_title,
            required_skills=request.required_skills,
            nice_to_have_skills=request.nice_to_have_skills or [],
            years_of_experience=request.years_of_experience,
            industry=request.industry,
            team_culture_description=request.team_culture_description,
            job_level=request.job_level,
            salary_range=request.salary_range,
            qualifications=request.qualifications
        )
        
        logger.info(f"✅ Job profile created: {request.role_title}")
        return {
            "status": "success",
            "profile": result['structured_profile'],
            "summary": result['summary'],
            "embedding_length": len(result.get('embedding', []))
        }
    except Exception as e:
        logger.error(f"Error creating hiring profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ===== Resume Parsing Endpoints =====

@app.post("/api/parse-resume")
async def parse_resume_text(request: ResumeParsingRequest):
    """Parse resume text and extract candidate information"""
    try:
        if not request.resume_text or len(request.resume_text.strip()) < 10:
            raise ValueError("Resume text is too short")
        
        logger.info("Parsing resume text...")
        result = resume_parser.parse_resume(request.resume_text)
        
        logger.info(f"✅ Resume parsed for candidate: {result['candidate_profile'].get('name', 'Unknown')}")
        return {
            "status": "success",
            "candidate": result['candidate_profile'],
            "embedding_length": len(result.get('embedding', []))
        }
    except Exception as e:
        logger.error(f"Resume parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/parse-resume/batch")
async def parse_resumes_batch(resumes: List[dict]):
    """Parse multiple resumes"""
    try:
        results = []
        for resume_item in resumes:
            try:
                result = resume_parser.parse_resume(resume_item.get('text', ''))
                results.append({
                    "status": "success",
                    "candidate": result['candidate_profile']
                })
            except Exception as e:
                results.append({"status": "error", "message": str(e)})
        
        logger.info(f"✅ Batch parsing complete: {len(results)} resumes processed")
        return {"results": results}
    except Exception as e:
        logger.error(f"Batch parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ===== Screening Endpoints =====

@app.post("/api/screening/generate-questions")
async def generate_screening_questions(request: ScreeningRequest):
    """Generate role-specific screening questions"""
    try:
        logger.info(f"Generating {request.num_questions} screening questions...")
        
        questions = screener.generate_screening_questions(
            request.hiring_profile,
            num_questions=request.num_questions
        )
        
        logger.info(f"✅ Generated {len(questions)} questions")
        return {
            "status": "success",
            "questions": [
                {
                    "id": q.question_id,
                    "text": q.question_text,
                    "category": q.category
                }
                for q in questions
            ]
        }
    except Exception as e:
        logger.error(f"Question generation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/screening/evaluate")
async def evaluate_screening_responses(request: ScreeningEvaluationRequest):
    """Evaluate candidate screening responses"""
    try:
        logger.info("Evaluating screening responses...")
        
        # Reconstruct screening questions
        from screening import ScreeningQuestion
        question_objs = [
            ScreeningQuestion(
                question_id=q['id'],
                question_text=q['text'],
                category=q.get('category', 'technical')
            )
            for q in request.questions
        ]
        
        result = screener.evaluate_responses(
            question_objs,
            request.answers,
            request.hiring_profile
        )
        
        logger.info(f"✅ Evaluation complete - Overall score: {result['overall_score']}/10")
        return {
            "status": "success",
            "scores": result['scores'],
            "overall_score": result['overall_score'],
            "reasoning": result['reasoning']
        }
    except Exception as e:
        logger.error(f"Screening evaluation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ===== Matching Endpoints =====

@app.post("/api/matching/compute")
async def compute_match(request: MatchingRequest):
    """Compute candidate-job match score"""
    try:
        logger.info("Computing candidate-job match...")
        
        # Use placeholder embeddings for now
        result = matcher.compute_match(
            hiring_embedding=[0.1] * 768,
            candidate_embedding=[0.1] * 768,
            screening_score=request.screening_score,
            candidate_profile=request.candidate_profile,
            hiring_profile=request.hiring_profile
        )
        
        logger.info(f"✅ Match computed - Score: {result['final_score']:.2f}/10")
        return {
            "status": "success",
            "similarity_score": result['similarity_score'],
            "screening_score": result['screening_score'],
            "final_score": result['final_score'],
            "explanation": result['explanation'],
            "recommendation": result['recommendation']
        }
    except Exception as e:
        logger.error(f"Matching error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/matching/batch")
async def match_batch_candidates(
    candidates: List[dict],
    hiring_profile: dict
):
    """Match multiple candidates with a job"""
    try:
        logger.info(f"Matching {len(candidates)} candidates...")
        
        results = []
        for candidate in candidates:
            try:
                match = matcher.compute_match(
                    hiring_embedding=[0.1] * 768,
                    candidate_embedding=[0.1] * 768,
                    screening_score=7.0,
                    candidate_profile=candidate,
                    hiring_profile=hiring_profile
                )
                results.append({
                    "status": "success",
                    "candidate_name": candidate.get('name', 'Unknown'),
                    **match
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "candidate_name": candidate.get('name', 'Unknown'),
                    "error": str(e)
                })
        
        logger.info(f"✅ Batch matching complete")
        return {"results": results}
    except Exception as e:
        logger.error(f"Batch matching error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ===== Feedback Endpoints =====

@app.post("/api/feedback/record")
async def record_feedback(request: FeedbackRequest):
    """Record hiring feedback for learning"""
    try:
        logger.info(f"Recording feedback for candidate {request.candidate_id}...")
        
        feedback_collector.record_feedback(
            candidate_id=request.candidate_id,
            hiring_manager_id=request.hiring_manager_id,
            final_score=request.final_score,
            feedback=request.feedback,  # "Good Fit" or "Not a Fit"
            notes=request.notes
        )
        
        logger.info("✅ Feedback recorded and weights adjusted")
        return {
            "status": "success",
            "message": "Feedback recorded",
            "current_weights": feedback_collector.get_weights()
        }
    except Exception as e:
        logger.error(f"Feedback recording error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/feedback/analytics")
async def get_analytics():
    """Get feedback analytics and model performance"""
    try:
        analytics = feedback_collector.get_feedback_analytics()
        weights = feedback_collector.get_weights()
        
        return {
            "status": "success",
            "analytics": analytics,
            "weights": weights
        }
    except Exception as e:
        logger.error(f"Analytics retrieval error: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/api/feedback/reset-weights")
async def reset_weights():
    """Reset model weights to defaults"""
    try:
        feedback_collector.reset_weights()
        logger.info("✅ Weights reset to defaults")
        return {
            "status": "success",
            "message": "Weights reset",
            "weights": feedback_collector.get_weights()
        }
    except Exception as e:
        logger.error(f"Reset weights error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ===== Error Handlers =====

@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    """Handle API errors"""
    logger.error(f"API Error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": str(exc)}
    )


@app.exception_handler(Exception)
async def general_error_handler(request, exc):
    """Handle general errors"""
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )


if __name__ == "__main__":
    try:
        logger.info(f"🚀 Starting TalentVector AI API...")
        logger.info(f"📍 Host: {Config.API_HOST}")
        logger.info(f"🔌 Port: {Config.API_PORT}")
        logger.info(f"🤖 Model: {Config.GEMINI_MODEL}")
        
        uvicorn.run(
            app,
            host=Config.API_HOST,
            port=Config.API_PORT,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"❌ Failed to start API: {str(e)}")
        sys.exit(1)
