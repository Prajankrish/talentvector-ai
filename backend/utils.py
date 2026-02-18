"""
Shared utilities, configuration management, and error handling for TalentVector AI.

This module provides:
- Centralized environment configuration management
- Custom exception hierarchy for semantic error handling
- Logging setup and configuration
- Decorators for error handling, input validation, and retry logic
- Utility functions for common operations
"""

import os
import json
import logging
import time
import functools
from typing import Any, Callable, Dict, List, Optional, Tuple
from pathlib import Path


# ===== Logging Setup =====

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a logger for a module.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               If None, uses LOG_LEVEL from environment.
    
    Returns:
        Configured logging.Logger instance
    
    Example:
        logger = setup_logger(__name__)
        logger.info("Starting module")
    """
    logger = logging.getLogger(name)
    
    # Get log level from environment or parameter
    log_level = level or Config.LOG_LEVEL
    level_int = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level_int)
    
    # Create console handler if not already present
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level_int)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# ===== Custom Exceptions =====

class TalentVectorException(Exception):
    """Base exception for all TalentVector AI errors."""
    pass


class ConfigurationError(TalentVectorException):
    """Raised when environment configuration is invalid or missing."""
    pass


class ResumeParsingError(TalentVectorException):
    """Raised when resume parsing fails."""
    pass


class ScreeningError(TalentVectorException):
    """Raised when screening evaluation fails."""
    pass


class MatchingError(TalentVectorException):
    """Raised when candidate matching fails."""
    pass


class DatabaseError(TalentVectorException):
    """Raised when database operations fail."""
    pass


class APIError(TalentVectorException):
    """Raised when external API calls fail."""
    pass


# ===== Configuration Management =====

class Config:
    """
    Centralized configuration management from environment variables.
    
    All configuration is read from .env file via python-dotenv.
    Provides typed access to environment variables with validation.
    
    Critical Variables:
        - GEMINI_API_KEY: Must be set via .env file
    
    Optional Variables (defaults provided):
        - GEMINI_MODEL: Default 'gemini-1.5-pro'
        - EMBEDDING_MODEL: Default 'models/embedding-001'
        - API_HOST: Default '0.0.0.0'
        - API_PORT: Default 8000
        - DATABASE_PATH: Default './data/talentvector.db'
        - FEEDBACK_DB_PATH: Default './data/feedback.db'
        - LOG_LEVEL: Default 'INFO'
        - MAX_RETRIES: Default 3
        - REQUEST_TIMEOUT: Default 30
    
    Example:
        is_valid, errors = Config.validate()
        if not is_valid:
            print(f"Config errors: {errors}")
            raise ConfigurationError(f"Invalid config: {errors}")
        
        api_key = Config.GEMINI_API_KEY
        model = Config.GEMINI_MODEL
    """
    
    # Critical configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Google Gemini Configuration
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/talentvector.db")
    FEEDBACK_DB_PATH = os.getenv("FEEDBACK_DB_PATH", "./data/feedback.db")
    
    # Application Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    @classmethod
    def validate(cls) -> Tuple[bool, List[str]]:
        """
        Validate critical configuration requirements.
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
            - is_valid: True if all critical config is present
            - errors: List of validation error messages
        
        Example:
            is_valid, errors = Config.validate()
            if not is_valid:
                raise ConfigurationError(f"Config errors: {errors}")
        """
        errors = []
        
        # Check critical configuration
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "":
            errors.append("GEMINI_API_KEY not set in environment")
        
        # Validate optional numeric configurations
        try:
            if cls.API_PORT <= 0 or cls.API_PORT > 65535:
                errors.append(f"API_PORT must be between 1 and 65535, got {cls.API_PORT}")
        except (ValueError, TypeError):
            errors.append(f"API_PORT must be an integer, got {cls.API_PORT}")
        
        try:
            if cls.MAX_RETRIES < 0:
                errors.append(f"MAX_RETRIES must be non-negative, got {cls.MAX_RETRIES}")
        except (ValueError, TypeError):
            errors.append(f"MAX_RETRIES must be an integer, got {cls.MAX_RETRIES}")
        
        try:
            if cls.REQUEST_TIMEOUT <= 0:
                errors.append(f"REQUEST_TIMEOUT must be positive, got {cls.REQUEST_TIMEOUT}")
        except (ValueError, TypeError):
            errors.append(f"REQUEST_TIMEOUT must be a number, got {cls.REQUEST_TIMEOUT}")
        
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL.upper() not in valid_levels:
            errors.append(f"LOG_LEVEL must be one of {valid_levels}, got {cls.LOG_LEVEL}")
        
        return (len(errors) == 0, errors)


# ===== Decorators =====

def handle_exceptions(logger: Optional[logging.Logger] = None) -> Callable:
    """
    Decorator to catch and log exceptions in functions.
    
    Args:
        logger: Optional logger instance. If provided, logs exceptions.
    
    Example:
        @handle_exceptions(logger)
        def risky_function(x):
            return 1 / x  # May raise ZeroDivisionError
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator


def validate_input(required_params: Optional[List[str]] = None) -> Callable:
    """
    Decorator to validate required input parameters.
    
    Args:
        required_params: List of parameter names that must be provided and non-empty.
                        If None, skips validation.
    
    Raises:
        ValueError: If any required parameter is missing or empty.
    
    Example:
        @validate_input(["name", "email"])
        def process_user(name, email):
            return f"Processing {name}"
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if required_params:
                for param in required_params:
                    if param not in kwargs and len(args) == 0:
                        raise ValueError(f"Required parameter '{param}' not provided")
                    
                    if param in kwargs and not kwargs[param]:
                        raise ValueError(f"Required parameter '{param}' cannot be empty")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_on_error(
    max_retries: Optional[int] = None,
    delay: float = 1.0,
    backoff: float = 1.0
) -> Callable:
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries. If None, uses Config.MAX_RETRIES.
        delay: Initial delay between retries in seconds.
        backoff: Multiplier for delay after each retry (exponential backoff).
    
    Raises:
        Exception: Re-raises the last exception after all retries exhausted.
    
    Example:
        @retry_on_error(max_retries=3, delay=2.0)
        def call_api():
            return requests.get("https://api.example.com")
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = max_retries if max_retries is not None else Config.MAX_RETRIES
            current_delay = delay
            last_exception = None
            
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        break
            
            raise last_exception
        return wrapper
    return decorator


# ===== Utility Functions =====

def safe_json_parse(json_string: str, default: Optional[Any] = None) -> Any:
    """
    Safely parse JSON string with fallback to default value.
    
    Args:
        json_string: JSON string to parse.
        default: Value to return if parsing fails. Defaults to empty dict.
    
    Returns:
        Parsed JSON object or default value on parse failure.
    
    Example:
        data = safe_json_parse('{"key": "value"}')
        data = safe_json_parse('invalid json', default={})
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else {}


def ensure_directory_exists(path: str) -> bool:
    """
    Create directory and all parent directories if they don't exist.
    
    Args:
        path: Directory path to create.
    
    Returns:
        True if directory exists (was created or already existed), False on error.
    
    Example:
        if ensure_directory_exists("./data"):
            print("Data directory ready")
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Failed to create directory {path}: {str(e)}")
        return False


def validate_score(score: float, minimum: float = 0.0, maximum: float = 10.0) -> bool:
    """
    Validate that a score is within expected range.
    
    Args:
        score: Score value to validate.
        minimum: Minimum acceptable score (inclusive).
        maximum: Maximum acceptable score (inclusive).
    
    Returns:
        True if score is within range, False otherwise.
    
    Example:
        if validate_score(7.5, 0, 10):
            print("Valid score")
    """
    try:
        return minimum <= float(score) <= maximum
    except (ValueError, TypeError):
        return False


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalize an embedding vector to unit length (L2 normalization).
    
    Args:
        embedding: List of float values representing an embedding.
    
    Returns:
        Normalized embedding vector with unit length.
        Returns original if length is 0 or normalization fails.
    
    Example:
        normalized = normalize_embedding([3.0, 4.0])  # Returns [0.6, 0.8]
    """
    try:
        import math
        magnitude = math.sqrt(sum(x**2 for x in embedding))
        if magnitude == 0:
            return embedding
        return [x / magnitude for x in embedding]
    except Exception:
        return embedding


# Module initialization
logger = setup_logger(__name__)

# Validate configuration on import
_is_valid, _errors = Config.validate()
if not _is_valid:
    logger.warning(f"Configuration validation issues: {_errors}")
