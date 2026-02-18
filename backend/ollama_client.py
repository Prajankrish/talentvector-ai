"""
Ollama Client for local LLM inference

Provides functions to interact with a local Ollama instance for:
- Text generation using llama3 model
- Embedding generation using nomic-embed-text model
"""

import requests
import json
import re
from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import setup_logger

logger = setup_logger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
GENERATE_MODEL = "mistral"
EMBEDDING_MODEL = "nomic-embed-text"
REQUEST_TIMEOUT = 900  # 15 minutes for local LLM inference (models can be slow on first run)


def safe_json_parse(text: str) -> Dict:
    """
    Safely extract and parse the first JSON object from text.
    
    Attempts to extract JSON from text that may contain markdown formatting,
    extra text, malformed structures, or incomplete data. Returns an empty dict 
    if parsing fails after all strategies.
    
    Uses 7-level fallback approach to handle various JSON malformations.
    
    Args:
        text (str): The text to parse for JSON content
        
    Returns:
        Dict: Parsed JSON as dictionary, or empty dict {} if parsing fails
        
    Examples:
        >>> safe_json_parse('{"name": "John"}')
        {'name': 'John'}
        
        >>> safe_json_parse('```json\n{"key": "value"}\n```')
        {'key': 'value'}
        
        >>> safe_json_parse('Some text {"data": 123} more text')
        {'data': 123}
        
        >>> safe_json_parse('invalid json')
        {}
    """
    if not text or not isinstance(text, str):
        logger.debug("safe_json_parse: Input is not a string")
        return {}
    
    text = text.strip()
    
    # Step 1: Try to parse the text as-is (valid JSON)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.debug(f"Step 1 failed: {str(e)[:80]}")
    
    # Step 2: Remove markdown code blocks (```json...``` format)
    if "```json" in text:
        try:
            json_str = text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (IndexError, json.JSONDecodeError) as e:
            logger.debug(f"Step 2 (json block) failed: {str(e)[:80]}")
    
    if "```" in text:
        try:
            parts = text.split("```")
            if len(parts) >= 3:
                json_str = parts[1].strip()
                return json.loads(json_str)
        except (IndexError, json.JSONDecodeError) as e:
            logger.debug(f"Step 2 (code block) failed: {str(e)[:80]}")
    
    # Step 3: Extract JSON using regex - find first { and matching }
    try:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.debug(f"Step 3 (regex extraction) failed: {str(e)[:80]}")
    
    # Step 4: Try to extract array if no object found
    try:
        match = re.search(r'\[[\s\S]*\]', text)
        if match:
            json_str = match.group(0)
            result = json.loads(json_str)
            return {"data": result}
    except json.JSONDecodeError as e:
        logger.debug(f"Step 4 (array extraction) failed: {str(e)[:80]}")
    
    # Step 5: Fix common JSON errors - trailing commas and newlines
    try:
        fixed_text = re.sub(r',(\s*[}\]])', r'\1', text)  # Remove trailing commas
        match = re.search(r'\{[\s\S]*\}', fixed_text)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except (json.JSONDecodeError, AttributeError) as e:
        logger.debug(f"Step 5 (lenient fix) failed: {str(e)[:80]}")
    
    # Step 6: Aggressive cleanup - remove common malformations
    try:
        # Remove extra newlines and spaces that might break structure
        cleaned = re.sub(r'(?<!\\)\\"', r'"', text)  # Fix escaped quotes
        cleaned = re.sub(r'\n\s*\n', ' ', cleaned)  # Remove extra newlines
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)  # Remove trailing commas again
        
        # Try to extract JSON
        match = re.search(r'\{[\s\S]*\}', cleaned)
        if match:
            json_str = match.group(0)
            # Try to fix missing quotes around keys (simple case: key: value)
            json_str = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
            return json.loads(json_str)
    except (json.JSONDecodeError, AttributeError) as e:
        logger.debug(f"Step 6 (aggressive cleanup) failed: {str(e)[:80]}")
    
    # Step 7: Last resort - try to extract and wrap nested structures
    try:
        # Look for any JSON-like structure and try to parse
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
        if match:
            json_str = match.group(0)
            # Remove trailing commas one more time
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            # Add quotes to unquoted keys
            json_str = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
    except (json.JSONDecodeError, AttributeError) as e:
        logger.debug(f"Step 7 (last resort) failed: {str(e)[:80]}")
    
    logger.debug(f"safe_json_parse: Failed to extract JSON after all strategies. Text length: {len(text)}")
    return {}


def generate_response(prompt: str) -> str:
    """
    Generate a text response using Ollama's llama3 model.
    
    Args:
        prompt (str): The input prompt for text generation
        
    Returns:
        str: The generated response text
        
    Raises:
        ConnectionError: If unable to connect to Ollama server
        ValueError: If the response is empty or invalid
        Exception: For other API errors
    """
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": GENERATE_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        logger.debug(f"Calling Ollama generate with model: {GENERATE_MODEL}")
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        if "response" not in data:
            raise ValueError("Invalid response format from Ollama: 'response' field missing")
        
        generated_text = data.get("response", "").strip()
        
        if not generated_text:
            raise ValueError("Ollama returned an empty response")
        
        logger.debug(f"Successfully generated response ({len(generated_text)} chars)")
        return generated_text
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: Unable to connect to Ollama at {OLLAMA_BASE_URL}")
        raise ConnectionError(
            f"Cannot connect to Ollama server at {OLLAMA_BASE_URL}. "
            "Make sure Ollama is running with: ollama serve"
        ) from e
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout: Request to Ollama exceeded {REQUEST_TIMEOUT}s")
        raise TimeoutError(
            f"Ollama request timed out after {REQUEST_TIMEOUT} seconds"
        ) from e
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {response.status_code}: {response.text}")
        raise Exception(f"Ollama API error: {response.status_code} - {response.text}") from e
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response from Ollama: {response.text}")
        raise Exception("Ollama returned invalid JSON response") from e
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_response: {str(e)}")
        raise


def generate_embedding(text: str) -> List[float]:
    """
    Generate embeddings for text using Ollama's nomic-embed-text model.
    
    Args:
        text (str): The input text to embed
        
    Returns:
        List[float]: The embedding vector as a list of floats
        
    Raises:
        ConnectionError: If unable to connect to Ollama server
        ValueError: If the text is empty or response is invalid
        Exception: For other API errors
    """
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    try:
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        payload = {
            "model": EMBEDDING_MODEL,
            "prompt": text
        }
        
        logger.debug(f"Calling Ollama embeddings with model: {EMBEDDING_MODEL}")
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        if "embedding" not in data:
            raise ValueError("Invalid response format from Ollama: 'embedding' field missing")
        
        embedding = data.get("embedding")
        
        if not isinstance(embedding, list):
            raise ValueError("Embedding is not a list")
        
        if not embedding:
            raise ValueError("Ollama returned an empty embedding")
        
        # Ensure all elements are floats
        embedding = [float(x) for x in embedding]
        
        logger.debug(f"Successfully generated embedding ({len(embedding)} dimensions)")
        return embedding
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: Unable to connect to Ollama at {OLLAMA_BASE_URL}")
        raise ConnectionError(
            f"Cannot connect to Ollama server at {OLLAMA_BASE_URL}. "
            "Make sure Ollama is running with: ollama serve"
        ) from e
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout: Request to Ollama exceeded {REQUEST_TIMEOUT}s")
        raise TimeoutError(
            f"Ollama request timed out after {REQUEST_TIMEOUT} seconds"
        ) from e
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {response.status_code}: {response.text}")
        raise Exception(f"Ollama API error: {response.status_code} - {response.text}") from e
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response from Ollama: {response.text}")
        raise Exception("Ollama returned invalid JSON response") from e
        
    except (ValueError, TypeError) as e:
        logger.error(f"Data validation error: {str(e)}")
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_embedding: {str(e)}")
        raise


if __name__ == "__main__":
    """Simple test script"""
    try:
        print("Testing generate_response...")
        response = generate_response("What is Python?")
        print(f"Response: {response[:100]}...")
        
        print("\nTesting generate_embedding...")
        embedding = generate_embedding("Hello world")
        print(f"Embedding dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        
    except Exception as e:
        print(f"Error: {e}")
