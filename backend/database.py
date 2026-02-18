"""
Database Module
SQLite database operations for candidates, jobs, and screening results.
"""

import sqlite3
import os
from typing import List, Optional
from datetime import datetime
from models import Candidate, JobPosition, ScreeningResult, MatchResult

class Database:
    """SQLite database management"""
    
    def __init__(self, db_path: str = "candidates.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def connect(self):
        """Create database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Candidates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                resume_text TEXT,
                embedding BLOB,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        # Job positions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                required_skills TEXT,
                required_experience INTEGER,
                embedding BLOB,
                created_at TIMESTAMP
            )
        """)
        
        # Screening results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screening_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                score REAL,
                recommendation TEXT,
                reasoning TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        
        # Match results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS match_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                similarity_score REAL,
                match_percentage REAL,
                reasoning TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_candidate(self, candidate: Candidate) -> str:
        """Add candidate to database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        candidate_id = candidate.id or datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO candidates (id, name, email, phone, resume_text, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_id,
            candidate.name,
            candidate.email,
            candidate.phone,
            candidate.resume_text,
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        return candidate_id
    
    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """Retrieve candidate from database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row if row else None
    
    def get_all_candidates(self) -> List[Candidate]:
        """Retrieve all candidates"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM candidates")
        rows = cursor.fetchall()
        conn.close()
        
        return list(rows) if rows else []
    
    def add_job(self, job: JobPosition) -> str:
        """Add job position to database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        job_id = job.id or datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO jobs (id, title, description, required_skills, required_experience, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            job.title,
            job.description,
            ",".join(job.required_skills),
            job.required_experience,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        return job_id
    
    def get_job(self, job_id: str) -> Optional[JobPosition]:
        """Retrieve job from database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row if row else None
