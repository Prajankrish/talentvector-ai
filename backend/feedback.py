"""
Feedback Module
Stores hiring feedback and dynamically adjusts matching weights using reinforcement learning.
"""

import sqlite3
import logging
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

from utils import setup_logger, Config, DatabaseError, ensure_directory_exists

logger = setup_logger(__name__)


class FeedbackEntry(BaseModel):
    """Feedback entry for hiring decision"""
    candidate_id: str
    hiring_manager_id: str
    final_score: float  # The score that was given
    feedback: str  # "Good Fit" or "Not a Fit"
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None


class WeightParameters(BaseModel):
    """Weight parameters for matching algorithm"""
    similarity_weight: float  # 0.0 to 1.0 (default 0.6)
    screening_weight: float  # 0.0 to 1.0 (default 0.4)
    adjusted_at: datetime
    confidence: float  # 0.0 to 1.0 - how confident we are in these weights


class FeedbackCollector:
    """Collect feedback and dynamically adjust matching weights using reinforcement learning"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize feedback collector with SQLite database.
        
        Args:
            db_path: Path to feedback database (uses Config.FEEDBACK_DB_PATH if None)
            
        Raises:
            DatabaseError: If database initialization fails
        """
        try:
            self.db_path = db_path or Config.FEEDBACK_DB_PATH
            
            # Ensure data directory exists
            import os
            data_dir = os.path.dirname(self.db_path)
            if data_dir and not ensure_directory_exists(data_dir):
                logger.warning(f"Could not create data directory: {data_dir}")
            
            self.init_database()
            
            # Current weight parameters (start with defaults)
            self.similarity_weight = 0.6
            self.screening_weight = 0.4
            self.confidence = 0.5  # Start with low confidence
            
            # Reinforcement learning parameters
            self.learning_rate = 0.05  # How quickly weights adjust
            self.min_feedback_for_adjustment = 5  # Minimum feedback entries before adjusting
            
            logger.info(f"FeedbackCollector initialized with database: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize FeedbackCollector: {str(e)}")
            raise DatabaseError(f"FeedbackCollector initialization failed: {str(e)}")
    
    def init_database(self):
        """
        Initialize SQLite database tables.
        
        Creates feedback and weight_history tables if they don't exist.
        
        Raises:
            DatabaseError: If database operations fail
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Feedback table - stores hiring decisions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT NOT NULL,
                    hiring_manager_id TEXT NOT NULL,
                    final_score REAL NOT NULL,
                    feedback TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Weight history table - tracks weight changes over time
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weight_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    similarity_weight REAL NOT NULL,
                    screening_weight REAL NOT NULL,
                    confidence REAL NOT NULL,
                    trigger_action TEXT,
                    feedback_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.debug(f"Database initialized successfully: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")
    
    def record_feedback(
        self,
        candidate_id: str,
        hiring_manager_id: str,
        final_score: float,
        feedback: str,
        notes: Optional[str] = None
    ) -> str:
        """
        Record hiring feedback and trigger weight adjustment.
        
        Args:
            candidate_id: Candidate identifier (required)
            hiring_manager_id: Hiring manager identifier (required)
            final_score: Final match score that was used (0-10)
            feedback: "Good Fit" or "Not a Fit" (required)
            notes: Optional feedback notes
            
        Returns:
            Feedback entry ID
            
        Raises:
            ValueError: If feedback value is invalid
            DatabaseError: If database operation fails
        """
        # Validate feedback
        if feedback not in ["Good Fit", "Not a Fit"]:
            raise ValueError("Feedback must be 'Good Fit' or 'Not a Fit'")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO feedback (candidate_id, hiring_manager_id, final_score, feedback, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (candidate_id, hiring_manager_id, final_score, feedback, notes))
            
            feedback_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Feedback recorded: {feedback} for {candidate_id}")
            
            # Check if we should adjust weights
            self._try_adjust_weights()
            
            return str(feedback_id)
        except Exception as e:
            logger.error(f"Failed to record feedback: {str(e)}")
            raise DatabaseError(f"Failed to record feedback: {str(e)}")
    
    def _try_adjust_weights(self):
        """
        Check if we have enough feedback to adjust weights.
        
        Triggers weight adjustment if minimum feedback threshold is reached.
        """
        try:
            feedback_count = self._get_feedback_count()
            
            if feedback_count >= self.min_feedback_for_adjustment:
                logger.info(f"Adjusting weights (feedback count: {feedback_count})")
                self._adjust_weights_based_on_feedback()
        except Exception as e:
            logger.error(f"Error in weight adjustment trigger: {str(e)}")
    
    def _adjust_weights_based_on_feedback(self):
        """
        Adjust weight parameters based on feedback using reinforcement learning.
        
        Logic:
        - Good Fit with high score: reinforce current weights
        - Not a Fit with high score: reduce weight on similarity (false positive)
        - Good Fit with low score: increase weight on screening (undervalued)
        - Not a Fit with low score: reduce weight on screening (consistent prediction)
        """
        try:
            # Get recent feedback
            feedback_data = self._get_recent_feedback(limit=10)
            
            if not feedback_data:
                return
            
            # Analyze feedback patterns
            good_fits = [f for f in feedback_data if f["feedback"] == "Good Fit"]
            not_fits = [f for f in feedback_data if f["feedback"] == "Not a Fit"]
            
            # Calculate average scores for each outcome
            avg_good_fit_score = (
                sum(f["final_score"] for f in good_fits) / len(good_fits)
                if good_fits else 5.0
            )
            avg_not_fit_score = (
                sum(f["final_score"] for f in not_fits) / len(not_fits)
                if not_fits else 5.0
            )
            
            # Initialize weight adjustments
            delta_similarity = 0.0
            delta_screening = 0.0
            trigger_action = ""
            
            # Pattern 1: High scores rejected (false positives - too much emphasis on similarity)
            if not_fits and avg_not_fit_score > 6.5:
                delta_similarity = -self.learning_rate
                delta_screening = self.learning_rate
                trigger_action = "Reduce similarity weight (false positives detected)"
            
            # Pattern 2: Low scores accepted (true positives - screening underweighted)
            elif good_fits and avg_good_fit_score < 5.0:
                delta_screening = self.learning_rate * 0.5
                delta_similarity = -self.learning_rate * 0.25
                trigger_action = "Increase screening weight (good low-score candidates)"
            
            # Pattern 3: High scores accepted (reinforce current weights)
            elif good_fits and avg_good_fit_score > 7.5:
                delta_similarity = self.learning_rate * 0.3
                delta_screening = self.learning_rate * 0.2
                trigger_action = "Reinforce current weights (strong matches)"
                self.confidence = min(0.95, self.confidence + 0.1)
            
            # Pattern 4: Low scores rejected (consistent - maintain but increase confidence)
            elif not_fits and avg_not_fit_score < 5.0:
                trigger_action = "Low scores consistently rejected (good filtering)"
                self.confidence = min(0.95, self.confidence + 0.05)
            
            # Apply weight adjustments
            if delta_similarity != 0 or delta_screening != 0:
                self.similarity_weight = max(0.3, min(0.8, self.similarity_weight + delta_similarity))
                self.screening_weight = max(0.2, min(0.7, self.screening_weight + delta_screening))
                
                # Ensure weights sum to reasonable value
                total = self.similarity_weight + self.screening_weight
                if total > 0:
                    self.similarity_weight /= total
                    self.screening_weight /= total
            
            # Record weight adjustment
            self._record_weight_adjustment(trigger_action, len(feedback_data))
            logger.info(f"Weights adjusted: {trigger_action}")
        except Exception as e:
            logger.error(f"Error adjusting weights: {str(e)}")
    
    def _record_weight_adjustment(self, trigger_action: str, feedback_count: int):
        """
        Record weight adjustment in history.
        
        Args:
            trigger_action: Description of what triggered the adjustment
            feedback_count: Number of feedback entries that triggered this
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO weight_history (similarity_weight, screening_weight, confidence, trigger_action, feedback_count)
                VALUES (?, ?, ?, ?, ?)
            """, (self.similarity_weight, self.screening_weight, self.confidence, trigger_action, feedback_count))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to record weight adjustment: {str(e)}")
    
    def _get_feedback_count(self) -> int:
        """
        Get total count of feedback entries.
        
        Returns:
            Total number of feedback records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM feedback")
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Failed to get feedback count: {str(e)}")
            return 0
    
    def _get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """
        Get recent feedback entries.
        
        Args:
            limit: Maximum number of recent entries to retrieve
            
        Returns:
            List of feedback dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT candidate_id, hiring_manager_id, final_score, feedback, notes, created_at
                FROM feedback
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "candidate_id": row[0],
                    "hiring_manager_id": row[1],
                    "final_score": row[2],
                    "feedback": row[3],
                    "notes": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve recent feedback: {str(e)}")
            return []
    
    def get_weights(self) -> Dict:
        """
        Get current weight parameters.
        
        Returns:
            Dict with current weight configuration
        """
        return {
            "similarity_weight": round(self.similarity_weight, 3),
            "screening_weight": round(self.screening_weight, 3),
            "confidence": round(self.confidence, 3),
            "total_feedback": self._get_feedback_count(),
            "updated_at": datetime.now().isoformat()
        }
    
    def get_weight_history(self, limit: int = 20) -> List[Dict]:
        """
        Get weight adjustment history.
        
        Args:
            limit: Maximum number of history entries to retrieve
            
        Returns:
            List of weight adjustment records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT similarity_weight, screening_weight, confidence, trigger_action, feedback_count, created_at
                FROM weight_history
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "similarity_weight": row[0],
                    "screening_weight": row[1],
                    "confidence": row[2],
                    "trigger_action": row[3],
                    "feedback_count": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to retrieve weight history: {str(e)}")
            return []
    
    def get_feedback_analytics(self) -> Dict:
        """
        Get analytics about feedback data.
        
        Returns:
            Dictionary with analytics including counts, percentages, and statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total feedback count
            cursor.execute("SELECT COUNT(*) FROM feedback")
            total = cursor.fetchone()[0]
            
            # Good Fit vs Not a Fit ratio
            cursor.execute("SELECT feedback, COUNT(*) FROM feedback GROUP BY feedback")
            feedback_counts = dict(cursor.fetchall())
            
            # Average score by feedback
            cursor.execute("""
                SELECT feedback, AVG(final_score), COUNT(*)
                FROM feedback
                GROUP BY feedback
            """)
            score_stats = cursor.fetchall()
            
            conn.close()
            
            # Prepare analytics
            good_fit_count = feedback_counts.get("Good Fit", 0)
            not_fit_count = feedback_counts.get("Not a Fit", 0)
            
            return {
                "total_feedback": total,
                "good_fit_count": good_fit_count,
                "not_fit_count": not_fit_count,
                "good_fit_percentage": round(good_fit_count / total * 100, 1) if total > 0 else 0,
                "score_statistics": [
                    {
                        "feedback": stat[0],
                        "avg_score": round(stat[1], 2),
                        "count": stat[2]
                    }
                    for stat in score_stats
                ],
                "current_weights": self.get_weights()
            }
        except Exception as e:
            logger.error(f"Failed to retrieve analytics: {str(e)}")
            return {
                "total_feedback": 0,
                "error": str(e)
            }
    
    def reset_weights(self):
        """Reset weights to default values."""
        self.similarity_weight = 0.6
        self.screening_weight = 0.4
        self.confidence = 0.5
        self._record_weight_adjustment("Manual reset to defaults", self._get_feedback_count())
        logger.info("Weights reset to defaults")
    
    def export_feedback_data(self) -> List[Dict]:
        """
        Export all feedback data.
        
        Returns:
            List of all feedback records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT candidate_id, hiring_manager_id, final_score, feedback, notes, created_at
                FROM feedback
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "candidate_id": row[0],
                    "hiring_manager_id": row[1],
                    "final_score": row[2],
                    "feedback": row[3],
                    "notes": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Failed to export feedback data: {str(e)}")
            return []
