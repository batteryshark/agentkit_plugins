"""
Google Web Search Tool
Powered by Google Gemini API with grounding support
"""
import os
import json
import time
import requests
import re
import logging
from typing import Dict, List, Optional, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google import genai
from google.genai import types

# Configure logging
logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    """Custom exception for rate limit errors."""
    pass

def extract_title_from_html(html_content: str) -> Optional[str]:
    """Extract title from HTML content using regex."""
    try:
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        return title_match.group(1).strip() if title_match else None
    except Exception:
        return None

def follow_redirect(url: str, timeout: int = 10) -> tuple[str, Optional[str]]:
    """Follow a URL redirect and return the final URL and page title."""
    try:
        # First try HEAD request to follow redirects
        head_response = requests.head(url, allow_redirects=True, timeout=timeout)
        final_url = head_response.url
        
        # Then get content to extract title
        response = requests.get(final_url, stream=True, timeout=timeout)
        content = next(response.iter_content(8192)).decode('utf-8', errors='ignore')
        response.close()
        
        title = extract_title_from_html(content)
        
        # Filter out Cloudflare and other protection pages
        if title and any(phrase in title for phrase in [
            "Attention Required! | Cloudflare",
            "Just a moment...",
            "Security check",
            "Access denied"
        ]):
            return final_url, None
            
        return final_url, title
    except Exception as e:
        logger.debug(f"Error following redirect for {url}: {e}")
        return url, None

def extract_references(response, max_references: int = 10) -> List[Dict]:
    """Extract detailed references from Gemini response."""
    try:
        # Convert response to raw format to access grounding metadata
        raw_response = json.loads(response.model_dump_json())
        
        if "candidates" not in raw_response or not raw_response["candidates"]:
            return []
            
        candidate = raw_response["candidates"][0]
        if "grounding_metadata" not in candidate:
            return []
            
        grounding_metadata = candidate["grounding_metadata"]
        references = []
        
        for support in grounding_metadata.get("grounding_supports", []):
            if len(references) >= max_references:
                break
                
            for chunk_idx in support.get("grounding_chunk_indices", []):
                if chunk_idx >= len(grounding_metadata.get("grounding_chunks", [])):
                    continue
                    
                chunk = grounding_metadata["grounding_chunks"][chunk_idx]
                if "web" in chunk:
                    # Follow URL and get actual title
                    url = chunk["web"]["uri"]
                    final_url, actual_title = follow_redirect(
                        url, 
                        timeout=int(os.getenv("GOOGLE_WEBSEARCH_TIMEOUT", "10"))
                    )
                    
                    reference = {
                        "content": support["segment"]["text"],
                        "url": final_url,
                        "title": actual_title or chunk["web"].get("title", "")
                    }
                    
                    # Add confidence if available
                    if support.get("confidence_scores"):
                        reference["confidence"] = support["confidence_scores"][0]
                    
                    references.append(reference)
                    
                    if len(references) >= max_references:
                        break
        
        return references
    except Exception as e:
        logger.error(f"Error extracting references: {e}")
        return []

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((RateLimitError, Exception)),
    reraise=True
)
def _make_gemini_request(client, model: str, query: str) -> Any:
    """Make a request to Gemini API with retry logic."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=f"{query}",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response
    except Exception as e:
        error_str = str(e).lower()
        if "rate limit" in error_str or "quota" in error_str or "429" in error_str:
            logger.warning(f"Rate limit hit, will retry: {e}")
            raise RateLimitError(f"Rate limit exceeded: {e}")
        else:
            logger.error(f"Gemini API error: {e}")
            raise

def search_web(search_term: str) -> Dict[str, Any]:
    """
    Perform a web search using Google Gemini API with grounding.
    
    Args:
        search_term: The search query to process
        
    Returns:
        Dictionary containing search results and metadata
    """
    # Check if the tool is enabled
    if os.getenv("GOOGLE_WEBSEARCH_ENABLED", "true").lower() == "false":
        logger.info("Google web search is disabled")
        return {
            "status": "disabled",
            "message": "Google web search functionality is disabled"
        }
    
    # Check for API key
    api_key = os.getenv("GOOGLE_WEBSEARCH_API_KEY")
    if not api_key:
        logger.error("Google Gemini API key not provided")
        return {
            "status": "error",
            "error": "Google Gemini API key not provided. Please set GOOGLE_WEBSEARCH_API_KEY environment variable."
        }
    
    # Get configuration from environment variables
    model = os.getenv("GOOGLE_WEBSEARCH_MODEL", "gemini-2.0-flash")
    max_references = int(os.getenv("GOOGLE_WEBSEARCH_MAX_REFERENCES", "10"))
    
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Make the request with retry logic
        response = _make_gemini_request(client, model, search_term)
        
        # Extract metadata from response
        raw_response = json.loads(response.model_dump_json())
        
        # Get grounding metadata if available
        grounding_metadata = {}
        if ("candidates" in raw_response and 
            raw_response["candidates"] and 
            "grounding_metadata" in raw_response["candidates"][0]):
            grounding_metadata = raw_response["candidates"][0]["grounding_metadata"]
        
        # Extract references with detailed information
        references = extract_references(response, max_references=max_references)
        
        # Get search queries used
        search_queries = grounding_metadata.get("web_search_queries", [])
        
        # Return structured response
        return {
            "status": "success",
            "data": {
                "query": search_term,
                "search_queries": search_queries,
                "response": response.text,
                "references": references,
                "reference_count": len(references)
            }
        }
        
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded after retries: {e}")
        return {
            "status": "error",
            "error": f"Rate limit exceeded: {str(e)}. Please wait before making more requests."
        }
    except Exception as e:
        logger.error(f"Web search failed: {str(e)}")
        return {
            "status": "error",
            "error": f"Web search failed: {str(e)}"
        }

if __name__ == "__main__":
    # Test the function
    from dotenv import load_dotenv
    load_dotenv()
    
    result = search_web("latest developments in AI")
    print(json.dumps(result, indent=2))
