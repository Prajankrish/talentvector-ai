"""
Hiring Manager Module
Creates and manages hiring manager profiles with Ollama (llama3) integration.
"""

import json
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel

from utils import (
    setup_logger, Config, handle_exceptions, APIError,
    safe_json_parse, validate_score
)
from ollama_client import generate_response, generate_embedding, safe_json_parse as ollama_safe_json_parse

logger = setup_logger(__name__)

class HiringManagerProfile(BaseModel):
    """Structured hiring manager profile"""
    role_title: str
    required_skills: List[str]
    nice_to_have_skills: List[str]
    years_of_experience: int
    industry: str
    team_culture_description: str
    qualifications: Optional[str] = None
    job_level: Optional[str] = None
    salary_range: Optional[str] = None


class HiringManager:
    """Creates and processes hiring manager profiles with Ollama (llama3) integration"""
    
    def __init__(self):
        """
        Initialize Ollama client for local LLM inference.
        
        Raises:
            APIError: If Ollama connection fails
        """
        try:
            # Test Ollama connection by generating a simple response
            test_response = generate_response("Say 'ready'")
            logger.info("HiringManager initialized with Ollama (llama3)")
        except Exception as e:
            logger.error(f"Failed to initialize HiringManager: {str(e)}")
            raise APIError(f"Ollama initialization failed: {str(e)}")
    
    def process_hiring_input(
        self,
        role_title: str,
        required_skills: List[str],
        nice_to_have_skills: List[str],
        years_of_experience: int,
        industry: str,
        team_culture_description: str,
        qualifications: Optional[str] = None,
        job_level: Optional[str] = None,
        salary_range: Optional[str] = None
    ) -> Dict:
        """
        Process hiring manager input and generate structured profile with embeddings.
        
        Args:
            role_title: Job role title (required)
            required_skills: List of required technical skills (required)
            nice_to_have_skills: List of nice-to-have skills
            years_of_experience: Minimum years of experience required
            industry: Industry or domain (required)
            team_culture_description: Description of team culture and work environment (required)
            qualifications: Optional additional qualifications
            job_level: Optional job level (junior, mid, senior, lead)
            salary_range: Optional salary range
            
        Returns:
            Dict with structured_profile, summary, and embedding vector
            
        Raises:
            ValueError: If required inputs are invalid
            APIError: If OpenAI API call fails
        """
        # Validate required inputs
        if not role_title or not role_title.strip():
            raise ValueError("Role title cannot be empty")
        if not required_skills:
            raise ValueError("At least one required skill must be provided")
        if years_of_experience < 0:
            raise ValueError("Years of experience cannot be negative")
        if not industry or not industry.strip():
            raise ValueError("Industry cannot be empty")
        if not team_culture_description or not team_culture_description.strip():
            raise ValueError("Team culture description cannot be empty")
        
        logger.info(f"Processing hiring input for role: {role_title}")
        
        # Structure the input using OpenAI
        structured_profile = self._structure_profile(
            role_title,
            required_skills,
            nice_to_have_skills,
            years_of_experience,
            industry,
            team_culture_description,
            qualifications,
            job_level,
            salary_range
        )
        
        # Generate summary
        summary = self._generate_summary(structured_profile)
        
        # Generate embedding
        embedding = self._generate_embedding(summary)
        
        return {
            "structured_profile": structured_profile,
            "summary": summary,
            "embedding": embedding
        }
    
    def _structure_profile(
        self,
        role_title: str,
        required_skills: List[str],
        nice_to_have_skills: List[str],
        years_of_experience: int,
        industry: str,
        team_culture_description: str,
        qualifications: Optional[str] = None,
        job_level: Optional[str] = None,
        salary_range: Optional[str] = None
    ) -> Dict:
        """
        Use Ollama to structure and enhance the hiring profile
        
        Returns:
            Structured profile as dictionary
        """
        prompt = self._create_structuring_prompt(
            role_title,
            required_skills,
            nice_to_have_skills,
            years_of_experience,
            industry,
            team_culture_description,
            qualifications,
            job_level,
            salary_range
        )
        
        system_instruction = "You are an expert recruiter. Structure hiring requirements into a comprehensive JSON profile. Return ONLY valid JSON, no additional text or markdown."
        full_prompt = system_instruction + "\n\n" + prompt
        
        try:
            response_text = generate_response(full_prompt)
            
            # Extract JSON from response (handle potential markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON response
            structured_data = json.loads(response_text)
            logger.debug(f"Successfully structured hiring profile for {role_title}")
            return structured_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {str(e)}, using default structure")
            # Fallback to basic structure if JSON parsing fails
            return self._create_default_structure(
                role_title,
                required_skills,
                nice_to_have_skills,
                years_of_experience,
                industry,
                team_culture_description
            )
        except Exception as e:
            logger.error(f"Error structuring profile: {str(e)}")
            # Fallback to basic structure on any error
            return self._create_default_structure(
                role_title,
                required_skills,
                nice_to_have_skills,
                years_of_experience,
                industry,
                team_culture_description
            )
    
    def _create_structuring_prompt(
        self,
        role_title: str,
        required_skills: List[str],
        nice_to_have_skills: List[str],
        years_of_experience: int,
        industry: str,
        team_culture_description: str,
        qualifications: Optional[str] = None,
        job_level: Optional[str] = None,
        salary_range: Optional[str] = None
    ) -> str:
        """Create structuring prompt for Gemini"""
        return f"""
        Structure the following hiring requirements into a comprehensive JSON profile.
        Return ONLY valid JSON, no additional text.
        
        Input:
        - Role Title: {role_title}
        - Required Skills: {', '.join(required_skills)}
        - Nice-to-Have Skills: {', '.join(nice_to_have_skills)}
        - Years of Experience: {years_of_experience}
        - Industry: {industry}
        - Team Culture: {team_culture_description}
        - Qualifications: {qualifications or 'N/A'}
        - Job Level: {job_level or 'N/A'}
        - Salary Range: {salary_range or 'N/A'}
        
        Return JSON with these fields:
        {{
            "role_title": string,
            "job_level": string,
            "industry": string,
            "required_skills": [list of skills],
            "nice_to_have_skills": [list of skills],
            "years_of_experience": number,
            "team_culture": string,
            "qualifications": string,
            "salary_range": string,
            "key_responsibilities": [list],
            "ideal_candidate_profile": string,
            "success_metrics": [list]
        }}
        """
    
    def _create_default_structure(
        self,
        role_title: str,
        required_skills: List[str],
        nice_to_have_skills: List[str],
        years_of_experience: int,
        industry: str,
        team_culture_description: str
    ) -> Dict:
        """Create default structure when JSON parsing fails"""
        return {
            "role_title": role_title,
            "required_skills": required_skills,
            "nice_to_have_skills": nice_to_have_skills,
            "years_of_experience": years_of_experience,
            "industry": industry,
            "team_culture": team_culture_description,
            "key_responsibilities": [],
            "ideal_candidate_profile": "",
            "success_metrics": []
        }
    
    def _generate_summary(self, structured_profile: Dict) -> str:
        """
        Generate a concise summary of the hiring intent using Ollama
        
        Args:
            structured_profile: Structured hiring profile
            
        Returns:
            Summary string
        """
        prompt = self._create_summary_prompt(structured_profile)
        
        system_instruction = "You are an expert recruiter. Write concise, compelling job summaries. Reply with only the summary, no additional text."
        full_prompt = system_instruction + "\n\n" + prompt
        
        try:
            summary = generate_response(full_prompt)
            logger.debug("Successfully generated hiring profile summary")
            return summary.strip()
        except Exception as e:
            logger.warning(f"Failed to generate summary: {str(e)}, using default")
            # Fallback to basic summary
            return f"Position: {structured_profile.get('role_title', 'Unknown')} in {structured_profile.get('industry', 'Unknown')} industry"
    
    def _create_summary_prompt(self, structured_profile: Dict) -> str:
        """Create summary generation prompt"""
        return f"""
        Create a short, compelling 2-3 sentence summary of this job opportunity that will attract ideal candidates:
        
        Role: {structured_profile.get('role_title', '')}
        Industry: {structured_profile.get('industry', '')}
        Team Culture: {structured_profile.get('team_culture', '')}
        Key Skills: {', '.join(structured_profile.get('required_skills', [])[:5])}
        
        Write a summary that captures the essence of the opportunity and appeals to potential candidates.
        """
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for the hiring profile using Ollama
        
        Args:
            text: Text to embed (usually the summary)
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            embedding = generate_embedding(text)
            logger.debug(f"Successfully generated embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            # Return zero vector of expected size on error
            return [0.0] * 768  # nomic-embed-text returns 768-dimensional embeddings
    
    def batch_process_hiring_profiles(
        self,
        profiles: List[Dict]
    ) -> List[Dict]:
        """
        Process multiple hiring profiles in batch
        
        Args:
            profiles: List of hiring profile dictionaries
            
        Returns:
            List of processed profiles with embeddings
        """
        results = []
        
        for profile in profiles:
            result = self.process_hiring_input(
                role_title=profile.get("role_title", ""),
                required_skills=profile.get("required_skills", []),
                nice_to_have_skills=profile.get("nice_to_have_skills", []),
                years_of_experience=profile.get("years_of_experience", 0),
                industry=profile.get("industry", ""),
                team_culture_description=profile.get("team_culture_description", ""),
                qualifications=profile.get("qualifications"),
                job_level=profile.get("job_level"),
                salary_range=profile.get("salary_range")
            )
            results.append(result)
        
        return results
    
    def validate_hiring_input(
        self,
        role_title: str,
        required_skills: List[str],
        years_of_experience: int,
        industry: str
    ) -> tuple[bool, List[str]]:
        """
        Validate hiring input for required fields
        
        Args:
            role_title: Job role title
            required_skills: Required skills list
            years_of_experience: Years required
            industry: Industry field
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if not role_title or not role_title.strip():
            errors.append("Role title is required")
        
        if not required_skills or len(required_skills) == 0:
            errors.append("At least one required skill must be specified")
        
        if years_of_experience < 0:
            errors.append("Years of experience cannot be negative")
        
        if not industry or not industry.strip():
            errors.append("Industry is required")
        
        return len(errors) == 0, errors
