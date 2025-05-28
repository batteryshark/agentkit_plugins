# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Google Web Search",
    "description": "Web search functionality powered by Google Gemini API with grounding",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": [
        "google-genai>=0.3.0",
        "tenacity>=8.0.0",
        "requests>=2.25.0",
        "aiohttp>=3.8.0"
    ],
    "environment_variables": {
        "GOOGLE_WEBSEARCH_API_KEY": {
            "description": "Google Gemini API key for web search",
            "default": "",
            "required": True
        },
        "GOOGLE_WEBSEARCH_ENABLED": {
            "description": "Enable/disable web search functionality",
            "default": "true",
            "required": False
        },
        "GOOGLE_WEBSEARCH_MODEL": {
            "description": "Gemini model to use for web search",
            "default": "gemini-2.0-flash",
            "required": False
        },
        "GOOGLE_WEBSEARCH_MAX_REFERENCES": {
            "description": "Maximum number of references to return",
            "default": "10",
            "required": False
        },
        "GOOGLE_WEBSEARCH_TIMEOUT": {
            "description": "Request timeout in seconds",
            "default": "10",
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================
# =============================================================================
# START OF EXPORTS
# =============================================================================
from .search_web import search_web
_module_exports = {
    "tools": [search_web]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 