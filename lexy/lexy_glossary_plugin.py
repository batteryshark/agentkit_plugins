# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Lexy Glossary Plugin",
    "description": "AI-powered glossary search and lookup tools with exact, fuzzy, and semantic search capabilities",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": [
        "pydantic>=2.0.0", 
        "rapidfuzz>=3.0.0",
        "PyYAML>=6.0.0"
    ],
    "environment_variables": {
        "LEXY_GLOSSARY_PATH": {
            "description": "Path to the YAML glossary file",
            "default": "glossary.yaml",
            "required": False
        },
        "LEXY_LLM_MODEL": {
            "description": "AI model for semantic search (e.g., gemini-2.0-flash or gpt-4o)",
            "default": "gemini-2.0-flash",
            "required": False
        },       
        "LEXY_LLM_GEMINI_API_KEY": {
            "description": "LLM API key for Gemini models",
            "default": None,
            "required": False
        },       
        "LEXY_LLM_OPENAI_API_KEY": {
            "description": "LLM API key for OpenAI models",
            "default": None,
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

import os
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field
from rapidfuzz import fuzz, process

# =============================================================================
# DATA MODELS
# =============================================================================

class Definition(BaseModel):
    """A single definition with its own see-also references."""
    text: str
    see_also: List[str] = []


class GlossaryTerm(BaseModel):
    """A single glossary term with definitions and see-also references."""
    term: str
    definitions: List[Definition]


class TermResult(BaseModel):
    """A term result with metadata."""
    term: str
    definitions: List[Definition]
    confidence: float = 1.0  # 1.0 for exact matches, <1.0 for fuzzy matches
    match_type: str = "exact"  # "exact", "fuzzy", "suggestion", "agentic"
    
    @property
    def all_see_also(self) -> List[str]:
        """Get all see-also terms from all definitions."""
        all_terms = []
        for definition in self.definitions:
            all_terms.extend(definition.see_also)
        return list(set(all_terms))  # Remove duplicates
    
    @property
    def definition_texts(self) -> List[str]:
        """Get just the definition text strings for backward compatibility."""
        return [definition.text for definition in self.definitions]


# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Configuration settings for Lexy."""
    
    @classmethod
    @property
    def LLM_MODEL(cls) -> str:
        """AI model for semantic search."""
        return os.getenv("LEXY_LLM_MODEL", _module_info["environment_variables"]["LEXY_LLM_MODEL"]["default"])
    
    @classmethod
    @property
    def LLM_API_KEY(cls) -> str:
        """LLM API key."""
        if cls.LLM_MODEL.startswith("gemini"):
            return os.getenv("LEXY_LLM_GEMINI_API_KEY")
        elif cls.LLM_MODEL.startswith("gpt"):
            return os.getenv("LEXY_LLM_OPENAI_API_KEY")
        else:
            return None
    
    @classmethod
    @property
    def GLOSSARY_PATH(cls) -> str:
        """Path to the glossary file."""
        return os.getenv("LEXY_GLOSSARY_PATH", _module_info["environment_variables"]["LEXY_GLOSSARY_PATH"]["default"])
    
    @classmethod
    def has_api_key_for_model(cls, model: str) -> bool:
        """Check if we have the required API key for the given model."""
        if model.startswith(("gemini")):
            return cls.LLM_API_KEY is not None
        return False


# =============================================================================
# GLOSSARY MANAGER
# =============================================================================

class GlossaryManager:
    """Manages loading and accessing glossary data."""
    
    def __init__(self, glossary_path: str):
        self.glossary_path = glossary_path
        self.glossary: Dict[str, Dict[str, Any]] = {}
        self.normalized_terms: Dict[str, str] = {}  # lowercase -> original case
        self.all_searchable_terms: List[str] = []  # For search processing
        self.load_glossary()
    
    def load_glossary(self):
        """Load glossary from YAML file."""
        try:
            if Path(self.glossary_path).exists():
                with open(self.glossary_path, 'r', encoding='utf-8') as f:
                    self.glossary = yaml.safe_load(f)
                        
                self._build_search_indexes()
                print(f"Loaded {len(self.glossary)} terms from {self.glossary_path}")
            else:
                print(f"Glossary file {self.glossary_path} not found, starting with empty glossary")
        except Exception as e:
            print(f"Error loading glossary: {e}")
            self.glossary = {}
            self.normalized_terms = {}
            self.all_searchable_terms = []
    
    def _build_search_indexes(self):
        """Build normalized lookup and searchable terms list."""
        self.normalized_terms = {}
        self.all_searchable_terms = []
        
        for term in self.glossary.keys():
            # Add main term
            self.normalized_terms[term.lower()] = term
            self.all_searchable_terms.append(term)
            
            # Add see-also terms for reverse lookup
            term_data = self.glossary[term]
            for definition in term_data.get('definitions', []):
                if isinstance(definition, dict) and 'see_also' in definition:
                    for see_also in definition['see_also']:
                        self.normalized_terms[see_also.lower()] = term
                        self.all_searchable_terms.append(see_also)
    
    def get_term_data(self, term: str) -> Dict[str, Any]:
        """Get raw term data from glossary."""
        return self.glossary.get(term, {})
    
    def get_term_object(self, term: str) -> GlossaryTerm:
        """Get a GlossaryTerm object from the new format."""
        term_data = self.get_term_data(term)
        if not term_data:
            return GlossaryTerm(term=term, definitions=[])
        
        # Convert dict definitions to Definition objects
        definitions = []
        for def_data in term_data.get('definitions', []):
            if isinstance(def_data, dict):
                definitions.append(Definition(
                    text=def_data.get('text', ''),
                    see_also=def_data.get('see_also', [])
                ))
            else:
                # Fallback for unexpected format
                definitions.append(Definition(text=str(def_data), see_also=[]))
        
        return GlossaryTerm(term=term, definitions=definitions)
    
    def term_exists(self, term: str) -> bool:
        """Check if a term exists in the glossary."""
        return term in self.glossary
    
    def get_original_term(self, normalized_term: str) -> str:
        """Get original term from normalized (lowercase) version."""
        return self.normalized_terms.get(normalized_term.lower(), normalized_term)
    
    def list_terms(self, prefix: str = None) -> List[str]:
        """List available terms with optional prefix filtering."""
        terms = list(self.glossary.keys())
        
        if prefix:
            prefix_lower = prefix.lower()
            terms = [term for term in terms if term.lower().startswith(prefix_lower)]
        
        return sorted(terms)
    
    def get_all_terms_text(self) -> str:
        """Get all terms and definitions as text for AI processing."""
        text_parts = []
        for term in self.glossary.keys():
            term_obj = self.get_term_object(term)
            definitions_text = "; ".join([def_.text for def_ in term_obj.definitions])
            text_parts.append(f"{term}: {definitions_text}")
            
            # Add see-also information
            all_see_also = []
            for definition in term_obj.definitions:
                all_see_also.extend(definition.see_also)
            
            if all_see_also:
                unique_see_also = list(set(all_see_also))
                text_parts.append(f"  (See also: {', '.join(unique_see_also)})")
        
        return "\n".join(text_parts)


# =============================================================================
# SEARCH CLASSES
# =============================================================================

class ExactSearch:
    """Handles exact term lookups with case-insensitive matching."""
    
    def __init__(self, glossary_manager: GlossaryManager):
        self.glossary = glossary_manager
    
    def lookup(self, term: str) -> List[TermResult]:
        """Exact term lookup with case-insensitive matching."""
        normalized_term = term.lower()
        
        if normalized_term in self.glossary.normalized_terms:
            original_term = self.glossary.normalized_terms[normalized_term]
            term_obj = self.glossary.get_term_object(original_term)
            
            return [TermResult(
                term=original_term,
                definitions=term_obj.definitions,
                confidence=1.0,
                match_type="exact"
            )]
        
        # If not found, provide fuzzy suggestions as potential matches
        fuzzy_search = FuzzySearch(self.glossary)
        suggestions = fuzzy_search.search(term, threshold=60)[:3]  # Top 3 suggestions
        
        # Mark them as suggestions
        for suggestion in suggestions:
            suggestion.match_type = "suggestion"
        
        return suggestions


class FuzzySearch:
    """Handles fuzzy matching using rapidfuzz for typos and variations."""
    
    def __init__(self, glossary_manager: GlossaryManager):
        self.glossary = glossary_manager
    
    def search(self, query: str, threshold: int = 80) -> List[TermResult]:
        """Fuzzy search with similarity scoring using rapidfuzz."""
        if not self.glossary.all_searchable_terms:
            return []
        
        results = []
        seen_terms = set()
        
        # Use rapidfuzz to find matches
        matches = process.extract(
            query, 
            self.glossary.all_searchable_terms, 
            scorer=fuzz.WRatio,
            limit=10,  # Get more matches to filter
            score_cutoff=threshold
        )
        
        for match_text, score, _ in matches:
            # Get the original term this match belongs to
            original_term = self.glossary.get_original_term(match_text)
            
            # Avoid duplicates
            if original_term in seen_terms:
                continue
            seen_terms.add(original_term)
            
            # Only include if it's actually in our glossary
            if self.glossary.term_exists(original_term):
                term_obj = self.glossary.get_term_object(original_term)
                results.append(TermResult(
                    term=original_term,
                    definitions=term_obj.definitions,
                    confidence=score / 100.0,  # Convert to 0-1 scale
                    match_type="fuzzy"
                ))
        
        # Sort by confidence
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results


class AgenticSearch:
    """Handles AI-powered contextual search using PydanticAI."""
    
    def __init__(self, glossary_manager: GlossaryManager, model: str = "gemini-2.0-flash"):
        self.glossary = glossary_manager
        self.model = model
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the PydanticAI agent if possible."""
        if Config.LLM_API_KEY is None:
            print("No API key for model, skipping agent initialization")
            return
        
        try:
            from pydantic_ai import Agent, RunContext
            from pydantic_ai.models.gemini import GeminiModel
            from pydantic_ai.providers.google_gla import GoogleGLAProvider
            from pydantic_ai.models.openai import OpenAIModel
            from pydantic_ai.providers.openai import OpenAIProvider

            if self.model.startswith("gemini"):
                model = GeminiModel(self.model, provider=GoogleGLAProvider(api_key=Config.LLM_API_KEY))
            elif self.model.startswith("gpt"):
                model = OpenAIModel(self.model, provider=OpenAIProvider(api_key=Config.LLM_API_KEY))
            else:
                print(f"Unsupported model: {self.model}")
                return

            self.agent = Agent(
                model,
                deps_type=str,  # Will pass glossary text as dependency
                output_type=List[str],
                system_prompt=(
                    'You are a glossary search expert. Given a user query and a glossary of terms, '
                    'find the most relevant terms that match the user\'s intent. '
                    'Consider synonyms, related concepts, context, and partial matches. '
                    'Return a list of term names (exact matches from the glossary) that are most relevant. '
                    'Return at most 5 terms, ordered by relevance.'
                ),
            )

            @self.agent.tool
            async def search_glossary_content(ctx: RunContext[str], query: str) -> str:
                """Search through the glossary content for relevant terms."""
                return f"User query: {query}\n\nGlossary content:\n{ctx.deps}"
                
        except Exception as e:
            print(f"Warning: Could not initialize AI agent: {e}")
            self.agent = None
    
    async def search(self, query: str, context: Optional[str] = None) -> List[TermResult]:
        """AI-powered contextual search across the glossary."""
        if self.agent is None:
            # Fallback to fuzzy search
            print("AI agent not available, falling back to fuzzy search")
            fuzzy_search = FuzzySearch(self.glossary)
            results = fuzzy_search.search(query, threshold=60)[:3]
            # Mark as agentic fallback
            for result in results:
                result.match_type = "agentic_fallback"
            return results
        
        try:
            # Prepare the search query with context
            full_query = query
            if context:
                full_query = f"{query} (Context: {context})"
            
            # Get glossary content for AI analysis
            glossary_text = self.glossary.get_all_terms_text()
            
            # Run AI agent to find relevant terms
            result = await self.agent.run(full_query, deps=glossary_text)
            relevant_terms = result.output
            
            # Look up the full details for each relevant term
            responses = []
            
            for term in relevant_terms:
                if self.glossary.term_exists(term):
                    term_obj = self.glossary.get_term_object(term)
                    responses.append(TermResult(
                        term=term,
                        definitions=term_obj.definitions,
                        confidence=1.0,  # AI found it relevant
                        match_type="agentic"
                    ))
            
            return responses
            
        except Exception as e:
            print(f"Error in agentic search: {e}")
            # Fallback to fuzzy search
            fuzzy_search = FuzzySearch(self.glossary)
            results = fuzzy_search.search(query, threshold=60)[:3]
            # Mark as agentic fallback
            for result in results:
                result.match_type = "agentic_fallback"
            return results


# =============================================================================
# GLOBAL INSTANCES
# =============================================================================

# Global instances - initialized lazily
_glossary_manager = None
_exact_search = None
_fuzzy_search = None
_agentic_search = None
_initialized = False


def _ensure_initialized():
    """Ensure all global instances are initialized."""
    global _glossary_manager, _exact_search, _fuzzy_search, _agentic_search, _initialized
    
    if not _initialized:
        # Initialize components
        _glossary_manager = GlossaryManager(Config.GLOSSARY_PATH)
        _exact_search = ExactSearch(_glossary_manager)
        _fuzzy_search = FuzzySearch(_glossary_manager)
        _agentic_search = AgenticSearch(_glossary_manager, Config.LLM_MODEL)
        _initialized = True


def initialize_plugin():
    """
    Initialize the plugin with current environment variables.
    This should be called by agentkit after environment setup.
    """
    global _initialized
    _initialized = False  # Force re-initialization
    _ensure_initialized()
    print(f"Lexy Glossary Plugin initialized with glossary: {Config.GLOSSARY_PATH}")


def get_glossary_manager():
    """Get the glossary manager instance, initializing if needed."""
    _ensure_initialized()
    return _glossary_manager


def get_exact_search():
    """Get the exact search instance, initializing if needed."""
    _ensure_initialized()
    return _exact_search


def get_fuzzy_search():
    """Get the fuzzy search instance, initializing if needed."""
    _ensure_initialized()
    return _fuzzy_search


def get_agentic_search():
    """Get the agentic search instance, initializing if needed."""
    _ensure_initialized()
    return _agentic_search


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

async def lookup_term(
    term: Annotated[str, Field(description="The term to look up")]
) -> List[dict]:
    """
    Look up a specific term in the glossary with exact matching.
    
    Args:
        term: The term to look up
        
    Returns:
        List of matching terms (usually 1 for exact match, or suggestions if not found)
    """
    print(f"Tool 'lookup_term' called with: term='{term}'")
    
    results = get_exact_search().lookup(term)
    response = [result.model_dump() for result in results]
    
    if results and results[0].match_type == "exact":
        print(f"Exact match found: {results[0].term}")
    else:
        print(f"No exact match, returning {len(results)} suggestions")
    
    return response


async def batch_lookup_terms(
    terms: Annotated[List[str], Field(description="List of terms to look up")]
) -> dict:
    """
    Look up multiple terms at once to reduce round trips.
    
    Args:
        terms: List of terms to look up
        
    Returns:
        Dictionary mapping each term to its lookup results
    """
    print(f"Tool 'batch_lookup_terms' called with {len(terms)} terms: {terms}")
    
    results = {}
    for term in terms:
        lookup_results = get_exact_search().lookup(term)
        results[term] = [result.model_dump() for result in lookup_results]
    
    exact_matches = sum(1 for term_results in results.values() 
                      if term_results and term_results[0].get('match_type') == 'exact')
    print(f"Batch lookup completed: {exact_matches}/{len(terms)} exact matches found")
    
    return results


async def fuzzy_search_terms(
    query: Annotated[str, Field(description="The search query")],
    threshold: Annotated[int, Field(description="Similarity threshold (0-100)")] = 80
) -> List[dict]:
    """
    Search for terms using fuzzy matching for typos and variations.
    
    Args:
        query: The search query
        threshold: Similarity threshold (0-100), default 80
        
    Returns:
        List of matching terms with similarity scores
    """
    print(f"Tool 'fuzzy_search_terms' called with: query='{query}', threshold={threshold}")
    
    results = get_fuzzy_search().search(query, threshold)
    response = [result.model_dump() for result in results]
    
    print(f"Fuzzy search found {len(results)} matches")
    return response


async def smart_query(
    query: Annotated[str, Field(description="Natural language query describing what you're looking for")],
    context: Annotated[Optional[str], Field(description="Optional additional context to help with the search")] = None
) -> List[dict]:
    """
    AI-powered contextual search across the glossary using natural language.
    
    Args:
        query: Natural language query describing what you're looking for
        context: Optional additional context to help with the search
        
    Returns:
        List of relevant terms found by AI analysis
    """
    print(f"Tool 'smart_query' called with: query='{query}', context='{context}'")
    
    results = await get_agentic_search().search(query, context)
    response = [result.model_dump() for result in results]
    
    print(f"Smart query found {len(results)} relevant terms")
    return response


async def list_terms(
    prefix: Annotated[Optional[str], Field(description="Optional prefix to filter terms (case-insensitive)")] = None
) -> List[str]:
    """
    List available terms in the glossary with optional filtering.
    
    Args:
        prefix: Optional prefix to filter terms (case-insensitive)
        
    Returns:
        List of term names matching the filters
    """
    print(f"Tool 'list_terms' called with: prefix='{prefix}'")
    
    terms = get_glossary_manager().list_terms(prefix=prefix)
    
    print(f"Listed {len(terms)} terms")
    return terms


# =============================================================================
# MAIN FUNCTION FOR TESTING
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def test_plugin():
        print("Testing Lexy Glossary Plugin...")
        
        # Test exact lookup
        print("\n=== Testing exact lookup ===")
        result = await lookup_term("MCP")
        print(f"Lookup result: {result}")
        
        # Test fuzzy search
        print("\n=== Testing fuzzy search ===")
        result = await fuzzy_search_terms("mcP", 70)
        print(f"Fuzzy search result: {result}")
        
        # Test list terms
        print("\n=== Testing list terms ===")
        result = await list_terms("M")
        print(f"Terms starting with 'M': {result}")
        
        # Test smart query (if AI is available)
        print("\n=== Testing smart query ===")
        try:
            result = await smart_query("What is a protocol for AI models?")
            print(f"Smart query result: {result}")
        except Exception as e:
            print(f"Smart query failed (expected if no API key): {e}")

    asyncio.run(test_plugin())


# =============================================================================
# START OF EXPORTS
# =============================================================================
_module_exports = {
    "tools": [
        lookup_term,
        batch_lookup_terms,
        fuzzy_search_terms,
        smart_query,
        list_terms
    ],
    "init_function": initialize_plugin
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 