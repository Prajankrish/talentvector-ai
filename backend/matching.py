"""
Matching Module
Matches candidates with hiring profiles using embeddings and screening scores.
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel

from utils import (
    setup_logger, Config, handle_exceptions, APIError,
    MatchingError, validate_score
)

logger = setup_logger(__name__)

class MatchResult(BaseModel):
    """Candidate-job match result"""
    candidate_id: str
    hiring_profile_id: str
    similarity_score: float  # 0-1 (cosine similarity)
    screening_score: float  # 0-10 (normalized from screening)
    final_score: float  # 0-10 (weighted combination)
    explanation: str
    recommendation: str


class CandidateJobMatcher:
    """Match candidates with hiring profiles using embeddings and screening scores"""
    
    def __init__(self):
        """
        Initialize matcher with scoring weights.
        """
        # Weights for final score calculation
        self.similarity_weight = 0.6
        self.screening_weight = 0.4
        
        logger.info("CandidateJobMatcher initialized with sklearn cosine_similarity")
    
    def compute_match(
        self,
        hiring_embedding: List[float],
        candidate_embedding: List[float],
        screening_score: float,
        candidate_id: str = "",
        hiring_profile_id: str = "",
        candidate_profile: Optional[Dict] = None,
        hiring_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Compute match score between candidate and hiring profile
        
        Args:
            hiring_embedding: Embedding vector from hiring manager profile
            candidate_embedding: Embedding vector from candidate profile
            screening_score: Screening evaluation score (0-10)
            candidate_id: Optional candidate identifier
            hiring_profile_id: Optional hiring profile identifier
            candidate_profile: Optional candidate profile dict
            hiring_profile: Optional hiring profile dict
            
        Returns:
            Dict with similarity, screening, and final scores
        """
        # Validate inputs
        if not hiring_embedding or not candidate_embedding:
            raise ValueError("Both embeddings must be provided")
        
        if screening_score < 0 or screening_score > 10:
            raise ValueError("Screening score must be between 0 and 10")
        
        # Compute cosine similarity
        similarity_score = self._compute_cosine_similarity(
            hiring_embedding,
            candidate_embedding
        )
        
        # Normalize screening score to 0-1 range
        normalized_screening = screening_score / 10.0
        
        # Compute final score: 0.6 * similarity + 0.4 * normalized_screening
        final_score = (self.similarity_weight * similarity_score) + (self.screening_weight * normalized_screening)
        
        # Scale final score to 0-10 range
        final_score_scaled = final_score * 10
        
        # Get recommendation
        recommendation = self._get_recommendation(final_score_scaled)
        
        # Generate detailed explanation
        explanation = self._generate_explanation(
            similarity_score,
            screening_score,
            final_score_scaled,
            candidate_profile,
            hiring_profile
        )
        
        logger.debug(f"Match computed: similarity={similarity_score:.3f}, screening={screening_score:.1f}, final={final_score_scaled:.2f}")
        
        return {
            "similarity_score": round(similarity_score, 3),
            "screening_score": round(screening_score, 2),
            "final_score": round(final_score_scaled, 2),
            "recommendation": recommendation,
            "explanation": explanation,
            "candidate_id": candidate_id,
            "hiring_profile_id": hiring_profile_id
        }
    
    def _compute_cosine_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Compute cosine similarity between two embedding vectors using sklearn
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Convert to numpy arrays and reshape for sklearn
        arr1 = np.array(embedding1, dtype=np.float32).reshape(1, -1)
        arr2 = np.array(embedding2, dtype=np.float32).reshape(1, -1)
        
        # Compute cosine similarity using sklearn
        similarity = cosine_similarity(arr1, arr2)[0][0]
        
        # Normalize from -1 to 1 range to 0 to 1 range
        normalized_similarity = (similarity + 1) / 2
        
        return float(normalized_similarity)
    
    def _generate_explanation(self, similarity, screening_score, final_score, candidate_profile=None, hiring_profile=None) -> str:
        """
        Generate detailed explanation of match score
        
        Args:
            similarity: Cosine similarity score (0-1)
            screening_score: Screening evaluation score (0-10)
            final_score: Final combined score (0-10)
            candidate_profile: Optional candidate profile dict
            hiring_profile: Optional hiring profile dict
            
        Returns:
            Detailed explanation string
        """
        candidate_name = "Candidate"
        if candidate_profile:
            candidate_name = candidate_profile.get('name', 'Candidate')
        
        role = "role"
        if hiring_profile:
            role = hiring_profile.get('role_title', 'role')
        
        # Build explanation based on component scores
        parts = []
        
        # Similarity explanation
        if similarity >= 0.9:
            parts.append(f"Strong technical compatibility ({similarity:.0%})")
        elif similarity >= 0.7:
            parts.append(f"Good technical fit ({similarity:.0%})")
        elif similarity >= 0.5:
            parts.append(f"Moderate technical overlap ({similarity:.0%})")
        else:
            parts.append(f"Limited technical match ({similarity:.0%})")
        
        # Screening explanation
        if screening_score >= 8:
            parts.append(f"Excellent screening performance ({screening_score:.1f}/10)")
        elif screening_score >= 6:
            parts.append(f"Good screening results ({screening_score:.1f}/10)")
        elif screening_score >= 4:
            parts.append(f"Acceptable responses ({screening_score:.1f}/10)")
        else:
            parts.append(f"Poor screening performance ({screening_score:.1f}/10)")
        
        explanation = ". ".join(parts) + "."
        return explanation
    
    def _get_recommendation(self, final_score: float) -> str:
        """
        Get hiring recommendation based on final score
        
        Args:
            final_score: Final match score (0-10)
            
        Returns:
            Recommendation string
        """
        if final_score >= 8:
            return "STRONG MATCH - Recommend immediate interview/next round"
        elif final_score >= 7:
            return "GOOD MATCH - Recommend for consideration"
        elif final_score >= 6:
            return "MODERATE MATCH - Consider if other candidates limited"
        elif final_score >= 5:
            return "WEAK MATCH - Not recommended at this time"
        else:
            return "POOR MATCH - Do not recommend"
    
    def batch_match_candidates(
        self,
        hiring_embedding: List[float],
        candidates: List[Dict],
        hiring_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Match multiple candidates against a hiring profile
        
        Args:
            hiring_embedding: Hiring profile embedding
            candidates: List of dicts with candidate_embedding, screening_score, and optional profile
            hiring_profile: Optional hiring profile for context
            
        Returns:
            List of match results sorted by final score (descending)
        """
        results = []
        
        for candidate in candidates:
            try:
                result = self.compute_match(
                    hiring_embedding,
                    candidate.get("embedding", []),
                    candidate.get("screening_score", 5.0),
                    candidate.get("id", ""),
                    candidate.get("hiring_profile_id", ""),
                    candidate.get("profile"),
                    hiring_profile
                )
                results.append(result)
            except Exception as e:
                results.append({
                    "candidate_id": candidate.get("id", ""),
                    "error": str(e),
                    "final_score": -1
                })
        
        # Sort by final score descending
        results.sort(key=lambda x: x.get("final_score", -1), reverse=True)
        
        return results
    
    def get_top_matches(
        self,
        match_results: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Get top K matching candidates
        
        Args:
            match_results: List of match results
            top_k: Number of top results to return
            
        Returns:
            Top K results with best matches first
        """
        return sorted(
            match_results,
            key=lambda x: x.get("final_score", 0),
            reverse=True
        )[:top_k]
    
    def filter_by_threshold(
        self,
        match_results: List[Dict],
        min_score: float = 6.0
    ) -> List[Dict]:
        """
        Filter match results by minimum score threshold
        
        Args:
            match_results: List of match results
            min_score: Minimum final score to include
            
        Returns:
            Filtered results above threshold
        """
        return [r for r in match_results if r.get("final_score", 0) >= min_score]
    
    def get_match_statistics(self, match_results: List[Dict]) -> Dict:
        """
        Get statistics from match results
        
        Args:
            match_results: List of match results
            
        Returns:
            Statistics dictionary
        """
        if not match_results:
            return {
                "total_matches": 0,
                "average_score": 0.0,
                "max_score": 0.0,
                "min_score": 0.0
            }
        
        scores = [r.get("final_score", 0) for r in match_results if "final_score" in r]
        
        return {
            "total_matches": len(match_results),
            "average_score": round(np.mean(scores), 2),
            "max_score": round(max(scores), 2),
            "min_score": round(min(scores), 2),
            "matches_above_7": len([s for s in scores if s >= 7]),
            "matches_above_6": len([s for s in scores if s >= 6]),
            "strong_matches_percentage": round(len([s for s in scores if s >= 8]) / len(scores) * 100, 1) if scores else 0.0
        }
