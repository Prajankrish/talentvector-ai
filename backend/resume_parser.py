"""
Resume Parser Module
Extracts structured candidate information from resumes using Ollama (llama3).
"""

import json
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel

from utils import (
    setup_logger, Config, handle_exceptions, APIError,
    safe_json_parse, ResumeParsingError
)
from ollama_client import generate_response, generate_embedding, safe_json_parse as ollama_safe_json_parse

logger = setup_logger(__name__)

class CandidateProfile(BaseModel):
    """Structured candidate profile extracted from resume"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[Dict[str, str]]  # [{"skill": "Python", "proficiency": "expert"}]
    years_of_experience: int
    tech_stack: List[str]
    industry_exposure: List[str]
    key_projects: List[Dict[str, str]]  # [{"name": "...", "description": "...", "tech": "..."}]
    work_experience: List[Dict[str, str]]  # [{"company": "...", "position": "...", "duration": "..."}]
    education: Optional[List[Dict[str, str]]] = None
    summary: Optional[str] = None


class ResumeParser:
    """Parse resumes and extract structured candidate information using Ollama"""
    
    def __init__(self):
        """
        Initialize Ollama client for resume parsing.
        
        Raises:
            APIError: If Ollama connection fails
        """
        try:
            # Test Ollama connection by generating a simple response
            test_response = generate_response("Say 'ready'")
            logger.info("ResumeParser initialized with Ollama (llama3)")
        except Exception as e:
            logger.error(f"Failed to initialize ResumeParser: {str(e)}")
            raise APIError(f"Ollama initialization failed: {str(e)}")
    
    def parse_resume(self, resume_text: str) -> Dict:
        """
        Parse resume text and extract structured candidate information with embedding.
        
        Args:
            resume_text: Raw resume text to parse (required, non-empty)
            
        Returns:
            Dict with candidate_profile and embedding vector
            
        Raises:
            ValueError: If resume_text is empty or invalid
            ResumeParsingError: If OpenAI parsing fails
        """
        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text cannot be empty")
        
        try:
            logger.info("Starting resume parsing...")
            
            # Extract candidate profile using OpenAI
            candidate_profile = self._extract_candidate_profile(resume_text)
            
            # Generate embedding from candidate profile
            embedding = self._generate_profile_embedding(candidate_profile)
            
            logger.info(f"Resume successfully parsed for: {candidate_profile.get('name', 'Unknown')}")
            
            return {
                "candidate_profile": candidate_profile,
                "embedding": embedding
            }
        except Exception as e:
            logger.error(f"Resume parsing failed: {str(e)}")
            raise ResumeParsingError(f"Failed to parse resume: {str(e)}")
    
    def _extract_candidate_profile(self, resume_text: str) -> Dict:
        """
        Use Ollama to extract structured candidate profile from resume
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Structured candidate profile as dictionary
        """
        prompt = self._create_extraction_prompt(resume_text)
        
        # Clear, simple system instruction
        system_instruction = "You are a resume parser. Extract candidate information and return ONLY valid JSON. No text before or after the JSON."
        full_prompt = system_instruction + "\n\n" + prompt
        
        try:
            logger.debug("Starting Ollama extraction...")
            response_text = generate_response(full_prompt)
            logger.debug(f"Ollama response received ({len(response_text)} chars)")
            
            # Log first 500 chars of response for debugging
            if response_text:
                logger.debug(f"Response preview: {response_text[:500]}")
            
            # Use the safe_json_parse helper from ollama_client
            extracted_data = ollama_safe_json_parse(response_text)
            
            if extracted_data:
                logger.debug(f"Successfully extracted candidate profile with {len(extracted_data)} fields")
                # Ensure all fields have consistent structure
                extracted_data = self._ensure_structure_consistency(extracted_data)
                return extracted_data
            else:
                logger.warning(f"safe_json_parse returned empty dict after all strategies")
                logger.warning(f"Full response that failed parsing: {response_text[:1000]}")
                return self._create_default_profile(resume_text)
            
        except Exception as e:
            logger.error(f"Error extracting profile: {str(e)}")
            logger.error(f"Response text: {response_text[:500] if 'response_text' in locals() else 'N/A'}")
            # Fallback to basic structure on any error
            return self._create_default_profile(resume_text)
    
    def _create_extraction_prompt(self, resume_text: str) -> str:
        """Create extraction prompt for Ollama - OPTIMIZED for JSON reliability"""
        # Truncate to first 2000 chars for faster processing
        truncated_text = resume_text[:2000]
        
        # Use explicit, simple format to avoid JSON errors from llama3
        return f"""Extract candidate information from the resume below.

RESUME TEXT:
{truncated_text}

RETURN EXACTLY THIS JSON FORMAT (no additional text):
{{
  "name": "Full name from resume",
  "email": "email address if present, else null",
  "phone": "phone number if present, else null",
  "years_of_experience": 0,
  "summary": "Professional summary of candidate",
  "tech_stack": ["Technology", "languages", "frameworks"],
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "industry_exposure": ["Industry 1", "Industry 2"],
  "work_experience": [
    {{"company": "Company Name", "position": "Job Title", "duration": "2 years", "description": "Key responsibilities and achievements"}},
    {{"company": "Previous Company", "position": "Previous Role", "duration": "3 years", "description": "What they did"}}
  ],
  "education": [
    {{"degree": "Bachelor's", "field": "Computer Science", "institution": "University Name"}}
  ],
  "key_projects": [
    {{"name": "Project Name", "description": "What the project does", "tech": "Technologies used"}}
  ]
}}

RULES:
1. Return ONLY valid JSON, nothing else
2. Use null for missing values, not empty strings or empty arrays
3. work_experience MUST be array of objects with: company, position, duration, description
4. education MUST be array of objects with: degree, field, institution
5. key_projects MUST be array of objects with: name, description, tech
6. Use double quotes for all strings
7. No trailing commas
8. No extra text before or after JSON"""
    
    def _create_default_profile(self, resume_text: str) -> Dict:
        """Create default profile when JSON parsing fails"""
        return {
            "name": "Unknown",
            "email": None,
            "phone": None,
            "skills": [],
            "years_of_experience": 0,
            "tech_stack": [],
            "industry_exposure": [],
            "key_projects": [],
            "work_experience": [],
            "education": [],
            "summary": "Resume parsing encountered issues. Please review manually."
        }
    
    def _ensure_structure_consistency(self, profile: Dict) -> Dict:
        """Ensure all fields have consistent structure and handle edge cases"""
        try:
            # Ensure work_experience is list of dicts
            work_exp = profile.get('work_experience', [])
            if work_exp:
                if isinstance(work_exp, list):
                    if len(work_exp) > 0 and isinstance(work_exp[0], str):
                        # Convert string array to proper structure
                        profile['work_experience'] = [
                            {
                                "company": exp.split('@')[1].strip() if '@' in str(exp) else "Unknown",
                                "position": exp.split('@')[0].strip() if '@' in str(exp) else str(exp),
                                "duration": "N/A",
                                "description": ""
                            }
                            for exp in work_exp
                        ]
                    elif len(work_exp) > 0 and isinstance(work_exp[0], dict):
                        # Ensure all dicts have required keys
                        normalized_exp = []
                        for exp in work_exp:
                            normalized_exp.append({
                                "company": exp.get('company', 'Unknown'),
                                "position": exp.get('position', 'N/A'),
                                "duration": exp.get('duration', 'N/A'),
                                "description": exp.get('description', '')
                            })
                        profile['work_experience'] = normalized_exp
                else:
                    profile['work_experience'] = []
            else:
                profile['work_experience'] = []
            
            # Ensure education is list of dicts
            edu = profile.get('education', [])
            if edu:
                if isinstance(edu, list):
                    if len(edu) > 0 and isinstance(edu[0], str):
                        profile['education'] = [
                            {"degree": "Unknown", "field": "Unknown", "institution": str(e)}
                            for e in edu
                        ]
                    elif len(edu) > 0 and isinstance(edu[0], dict):
                        normalized_edu = []
                        for e in edu:
                            normalized_edu.append({
                                "degree": e.get('degree', 'Unknown'),
                                "field": e.get('field', 'Unknown'),
                                "institution": e.get('institution', 'Unknown')
                            })
                        profile['education'] = normalized_edu
                else:
                    profile['education'] = []
            else:
                profile['education'] = []
            
            # Ensure key_projects is list of dicts
            projects = profile.get('key_projects', [])
            if projects:
                if isinstance(projects, list):
                    if len(projects) > 0 and isinstance(projects[0], str):
                        profile['key_projects'] = [
                            {
                                "name": p.split(' - ')[0] if ' - ' in str(p) else str(p),
                                "description": "",
                                "tech": p.split(' - ')[1] if ' - ' in str(p) else "Unknown"
                            }
                            for p in projects
                        ]
                    elif len(projects) > 0 and isinstance(projects[0], dict):
                        normalized_proj = []
                        for p in projects:
                            normalized_proj.append({
                                "name": p.get('name', 'Unknown'),
                                "description": p.get('description', ''),
                                "tech": p.get('tech', 'Unknown')
                            })
                        profile['key_projects'] = normalized_proj
                else:
                    profile['key_projects'] = []
            else:
                profile['key_projects'] = []
        
        except Exception as e:
            logger.warning(f"Error in structure consistency check: {str(e)}")
            # Ensure basic structure exists
            profile.setdefault('work_experience', [])
            profile.setdefault('education', [])
            profile.setdefault('key_projects', [])
        
        return profile
    
    def _generate_profile_embedding(self, candidate_profile: Dict) -> List[float]:
        """
        Generate embedding vector from candidate profile using Ollama
        
        Args:
            candidate_profile: Structured candidate profile dictionary
            
        Returns:
            Embedding vector as list of floats
        """
        # Convert profile to text for embedding
        profile_text = self._profile_to_text(candidate_profile)
        
        try:
            embedding = generate_embedding(profile_text)
            logger.debug(f"Successfully generated candidate profile embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            # Return zero vector of expected size on error
            return [0.0] * 768  # nomic-embed-text returns 768-dimensional embeddings
    
    def _profile_to_text(self, candidate_profile: Dict) -> str:
        """
        Convert candidate profile to text for embedding
        
        Args:
            candidate_profile: Candidate profile dictionary
            
        Returns:
            Text representation of profile
        """
        # Safely extract tech stack
        tech_stack = candidate_profile.get("tech_stack", [])
        if isinstance(tech_stack, list):
            tech_stack_text = ", ".join(tech_stack[:5])
        else:
            tech_stack_text = str(tech_stack)
        
        # Safely extract industries
        industries = candidate_profile.get("industry_exposure", [])
        if isinstance(industries, list):
            industries_text = ", ".join(industries[:3])
        else:
            industries_text = str(industries)
        
        # Safely extract skills
        skills = candidate_profile.get("skills", [])
        if isinstance(skills, list):
            skills_text = ", ".join([s.get("skill", "") if isinstance(s, dict) else str(s) for s in skills[:5]])
        else:
            skills_text = str(skills)
        
        text = f"""
        Candidate: {candidate_profile.get('name', 'Unknown')}
        Email: {candidate_profile.get('email', 'Not provided')}
        Years of Experience: {candidate_profile.get('years_of_experience', 0)}
        Skills: {skills_text}
        Tech Stack: {tech_stack_text}
        Industries: {industries_text}
        Summary: {candidate_profile.get('summary', '')}
        """
        
        return text.strip()
    
    def batch_parse_resumes(self, resume_texts: List[str]) -> List[Dict]:
        """
        Parse multiple resumes in batch
        
        Args:
            resume_texts: List of resume texts
            
        Returns:
            List of parsed resume data with embeddings
        """
        results = []
        
        for resume_text in resume_texts:
            try:
                result = self.parse_resume(resume_text)
                results.append(result)
            except Exception as e:
                results.append({
                    "error": str(e),
                    "candidate_profile": None,
                    "embedding": None
                })
        
        return results
    
    def extract_skills(self, resume_text: str) -> List[Dict[str, str]]:
        """
        Extract only skills from resume
        
        Args:
            resume_text: Resume text
            
        Returns:
            List of skills with proficiency levels
        """
        profile = self._extract_candidate_profile(resume_text)
        return profile.get("skills", [])
    
    def extract_tech_stack(self, resume_text: str) -> List[str]:
        """
        Extract only tech stack from resume
        
        Args:
            resume_text: Resume text
            
        Returns:
            List of technologies
        """
        profile = self._extract_candidate_profile(resume_text)
        return profile.get("tech_stack", [])
    
    def extract_industries(self, resume_text: str) -> List[str]:
        """
        Extract only industry exposure from resume
        
        Args:
            resume_text: Resume text
            
        Returns:
            List of industries
        """
        profile = self._extract_candidate_profile(resume_text)
        return profile.get("industry_exposure", [])
    
    def extract_key_projects(self, resume_text: str) -> List[Dict[str, str]]:
        """
        Extract only key projects from resume
        
        Args:
            resume_text: Resume text
            
        Returns:
            List of key projects
        """
        profile = self._extract_candidate_profile(resume_text)
        return profile.get("key_projects", [])
    
    def get_total_experience_years(self, resume_text: str) -> int:
        """
        Get total years of experience from resume
        
        Args:
            resume_text: Resume text
            
        Returns:
            Total years of experience
        """
        profile = self._extract_candidate_profile(resume_text)
        return profile.get("years_of_experience", 0)
