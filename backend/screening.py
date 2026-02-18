"""
Screening Module
Generates role-specific screening questions and evaluates candidate answers using Ollama (llama3).
"""

import json
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel

from utils import (
    setup_logger, Config, handle_exceptions, APIError,
    safe_json_parse, ScreeningError, validate_score
)
from ollama_client import generate_response, safe_json_parse as ollama_safe_json_parse

logger = setup_logger(__name__)

class ScreeningQuestion(BaseModel):
    """Represents a screening question"""
    question_id: int
    question_text: str
    category: str  # technical, behavioral, problem-solving


class ScreeningScore(BaseModel):
    """Screening evaluation scores"""
    technical: int  # 0-10
    communication: int  # 0-10
    problem_solving: int  # 0-10
    overall_score: int  # 0-10
    reasoning: str


class CandidateScreener:
    """Generate screening questions and evaluate candidate responses using Ollama"""
    
    def __init__(self):
        """
        Initialize Ollama client for screening evaluation.
        
        Raises:
            APIError: If Ollama connection fails
        """
        try:
            # Test Ollama connection by generating a simple response
            test_response = generate_response("Say 'ready'")
            logger.info("CandidateScreener initialized with Ollama (llama3)")
        except Exception as e:
            logger.error(f"Failed to initialize CandidateScreener: {str(e)}")
            raise APIError(f"Ollama initialization failed: {str(e)}")
    
    def generate_screening_questions(
        self,
        hiring_profile: Dict,
        num_questions: int = 3
    ) -> List[ScreeningQuestion]:
        """
        Generate role-specific screening questions based on hiring profile
        
        Args:
            hiring_profile: Structured hiring manager profile
            num_questions: Number of questions to generate (3-5, default 3)
            
        Returns:
            List of ScreeningQuestion objects
        """
        if num_questions < 3 or num_questions > 5:
            num_questions = 3
        
        prompt = self._create_questions_prompt(hiring_profile, num_questions)
        
        system_instruction = "You are an expert technical interviewer. Generate insightful screening questions that assess technical depth, communication, and problem-solving. Return ONLY valid JSON with NO additional text."
        full_prompt = system_instruction + "\n\n" + prompt
        
        try:
            response_text = generate_response(full_prompt)
            
            # Use safe_json_parse helper from ollama_client
            questions_data = ollama_safe_json_parse(response_text)
            
            if not questions_data:
                logger.warning("safe_json_parse returned empty dict, using defaults")
                return self._create_default_questions(hiring_profile)
            
            questions = []
            
            for i, q in enumerate(questions_data.get("questions", [])[:num_questions], 1):
                if isinstance(q, dict):
                    question = ScreeningQuestion(
                        question_id=i,
                        question_text=q.get("question", ""),
                        category=q.get("category", "technical")
                    )
                    questions.append(question)
            
            logger.debug(f"Generated {len(questions)} screening questions")
            return questions if questions else self._create_default_questions(hiring_profile)
        
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Failed to parse screening questions: {str(e)}, using defaults")
            return self._create_default_questions(hiring_profile)
    
    def _create_questions_prompt(self, hiring_profile: Dict, num_questions: int) -> str:
        """Create prompt for question generation using Ollama"""
        role = hiring_profile.get("role_title", "")
        skills = hiring_profile.get("required_skills", [])
        team_culture = hiring_profile.get("team_culture", "")
        
        return f"""Generate exactly {num_questions} role-specific screening questions for a {role} position.

Required skills: {', '.join(skills[:5])}
Team culture: {team_culture}

Create a mix of technical, problem-solving, and communication questions.

Return ONLY valid JSON (no markdown, no extra text, no preamble):
{{
    "questions": [
        {{"question": "Question text here?", "category": "technical"}},
        {{"question": "Question text here?", "category": "problem_solving"}},
        {{"question": "Question text here?", "category": "communication"}}
    ]
}}

Make questions role-specific and realistic. Do not include any text outside the JSON braces."""
    
    def _create_default_questions(self, hiring_profile: Dict) -> List[ScreeningQuestion]:
        """Create default questions if JSON parsing fails"""
        role = hiring_profile.get("role_title", "Developer")
        
        return [
            ScreeningQuestion(
                question_id=1,
                question_text=f"Describe your most relevant experience as a {role}. What key achievements are you most proud of?",
                category="technical"
            ),
            ScreeningQuestion(
                question_id=2,
                question_text="Tell us about a challenging technical problem you solved. What was your approach and what did you learn?",
                category="problem_solving"
            ),
            ScreeningQuestion(
                question_id=3,
                question_text="How do you stay updated with new technologies and trends in your field? Give an example.",
                category="communication"
            )
        ]
    
    def evaluate_responses(
        self,
        questions: List[ScreeningQuestion],
        answers: Dict[int, str],
        hiring_profile: Dict,
        candidate_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Evaluate candidate responses to screening questions using Ollama
        
        Args:
            questions: List of ScreeningQuestion objects
            answers: Dict mapping question_id to answer text
            hiring_profile: Hiring manager profile for context
            candidate_profile: Optional candidate profile for additional context
            
        Returns:
            Dict with scores and reasoning
        """
        if not answers or len(answers) == 0:
            raise ValueError("No answers provided for evaluation")
        
        prompt = self._create_evaluation_prompt(
            questions,
            answers,
            hiring_profile,
            candidate_profile
        )
        
        system_instruction = "You are an expert technical interviewer and evaluator. Assess candidate responses objectively. Return ONLY valid JSON with NO additional text."
        full_prompt = system_instruction + "\n\n" + prompt
        
        try:
            response_text = generate_response(full_prompt)
            
            # Use safe_json_parse helper from ollama_client
            evaluation_data = ollama_safe_json_parse(response_text)
            
            if not evaluation_data:
                logger.warning("safe_json_parse returned empty dict, using defaults")
                return self._create_default_evaluation()
            
            technical = int(evaluation_data.get("technical_depth", 5))
            communication = int(evaluation_data.get("communication_clarity", 5))
            problem_solving = int(evaluation_data.get("problem_solving_ability", 5))
            
            # Clamp scores to 0-10
            technical = max(0, min(10, technical))
            communication = max(0, min(10, communication))
            problem_solving = max(0, min(10, problem_solving))
            
            # Calculate overall score as average
            overall = round((technical + communication + problem_solving) / 3)
            overall = max(0, min(10, overall))
            
            logger.debug(f"Evaluated candidate: Technical={technical}, Communication={communication}, ProblemSolving={problem_solving}, Overall={overall}")
            
            return {
                "scores": {
                    "technical": technical,
                    "communication": communication,
                    "problem_solving": problem_solving
                },
                "overall_score": overall,
                "reasoning": evaluation_data.get("reasoning", "")
            }
        
        except (json.JSONDecodeError, ValueError, KeyError, Exception) as e:
            logger.warning(f"Failed to parse evaluation JSON: {str(e)}, using defaults")
            return self._create_default_evaluation()
    
    def _create_evaluation_prompt(
        self,
        questions: List[ScreeningQuestion],
        answers: Dict[int, str],
        hiring_profile: Dict,
        candidate_profile: Optional[Dict] = None
    ) -> str:
        """Create evaluation prompt for Ollama"""
        
        # Build Q&A pairs
        qa_pairs = []
        for q in questions:
            answer_text = answers.get(q.question_id, "[No answer provided]")
            qa_pairs.append(f"Q{q.question_id}: {q.question_text}\nA{q.question_id}: {answer_text}")
        
        qa_text = "\n\n".join(qa_pairs)
        
        role = hiring_profile.get("role_title", "")
        required_skills = hiring_profile.get("required_skills", [])
        
        candidate_context = ""
        if candidate_profile:
            candidate_context = f"\nCandidate's Tech Skills: {', '.join(candidate_profile.get('tech_stack', [])[:5])}"
        
        return f"""Evaluate this screening interview for a {role} position.

Required Skills: {', '.join(required_skills)}
{candidate_context}

Interview:
{qa_text}

Score on these dimensions (0-10):
- technical_depth: Understanding of concepts and relevant experience
- communication_clarity: Ability to explain clearly
- problem_solving_ability: Approach to challenges and creativity

Return ONLY valid JSON (no markdown, no text outside braces):
{{
    "technical_depth": number,
    "communication_clarity": number,
    "problem_solving_ability": number,
    "reasoning": "Brief evaluation summary"
}}"""
    
    def _create_default_evaluation(self) -> Dict:
        """Create default evaluation if JSON parsing fails"""
        return {
            "scores": {
                "technical": 5,
                "communication": 5,
                "problem_solving": 5
            },
            "overall_score": 5,
            "reasoning": "Evaluation scoring encountered technical issues. Please review manually."
        }
    
    def screen_and_score(
        self,
        hiring_profile: Dict,
        candidate_answers: Dict[int, str],
        candidate_profile: Optional[Dict] = None,
        num_questions: int = 4
    ) -> Dict:
        """
        Complete screening workflow: generate questions and evaluate answers
        
        Args:
            hiring_profile: Hiring manager profile
            candidate_answers: Dict mapping question_id to answer text
            candidate_profile: Optional candidate profile
            num_questions: Number of questions to generate
            
        Returns:
            Combined dict with questions and evaluation scores
        """
        # Generate questions
        questions = self.generate_screening_questions(hiring_profile, num_questions)
        
        # Evaluate responses
        evaluation = self.evaluate_responses(
            questions,
            candidate_answers,
            hiring_profile,
            candidate_profile
        )
        
        return {
            "questions": [
                {
                    "id": q.question_id,
                    "text": q.question_text,
                    "category": q.category,
                    "answer": candidate_answers.get(q.question_id, "")
                }
                for q in questions
            ],
            **evaluation
        }
    
    def batch_screen_candidates(
        self,
        hiring_profile: Dict,
        candidates_responses: List[Dict],
        num_questions: int = 3
    ) -> List[Dict]:
        """
        Screen multiple candidates
        
        Args:
            hiring_profile: Hiring manager profile
            candidates_responses: List of dicts with candidate_profile and answers
            num_questions: Number of questions to evaluate each candidate on
            
        Returns:
            List of evaluation results for each candidate
        """
        results = []
        
        for candidate_data in candidates_responses:
            try:
                result = self.screen_and_score(
                    hiring_profile,
                    candidate_data.get("answers", {}),
                    candidate_data.get("profile", None),
                    num_questions
                )
                results.append(result)
            except Exception as e:
                results.append({
                    "error": str(e),
                    "scores": None,
                    "overall_score": None
                })
        
        return results
    
    def get_recommendation(self, overall_score: int) -> str:
        """
        Get hiring recommendation based on overall score
        
        Args:
            overall_score: Overall score (0-10)
            
        Returns:
            Recommendation string
        """
        if overall_score >= 8:
            return "STRONG YES - Excellent candidate. Recommend for next round."
        elif overall_score >= 7:
            return "YES - Good candidate. Recommend for next round."
        elif overall_score >= 6:
            return "MAYBE - Borderline candidate. Consider reviewing answers in detail."
        elif overall_score >= 5:
            return "UNLIKELY - Below average. Not recommended at this time."
        else:
            return "NO - Poor fit. Not recommended."
