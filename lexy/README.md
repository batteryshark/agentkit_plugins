# Lexy Glossary Plugin

AI-powered glossary search and lookup tools with exact, fuzzy, and semantic search capabilities.

![](logo.jpg "Lexy Logo")

## Overview

The Lexy Glossary Plugin provides intelligent search functionality for YAML-based glossaries. It offers multiple search modes including exact matching, fuzzy search for typos, and AI-powered semantic search for natural language queries.

## Features

- **Exact Term Lookup**: Case-insensitive exact matching with suggestions for near-misses
- **Fuzzy Search**: Typo-tolerant search using advanced string matching algorithms
- **AI-Powered Semantic Search**: Natural language queries powered by LLMs (Gemini/OpenAI)
- **Batch Operations**: Look up multiple terms efficiently in a single call
- **Term Listing**: Browse available terms with optional prefix filtering
- **See-Also References**: Navigate related terms and concepts

## Tool Calls

### `lookup_term`
Look up a specific term in the glossary with exact matching.

**Parameters:**
- `term` (string): The term to look up

**Returns:** List of matching terms (usually 1 for exact match, or suggestions if not found)

**Example:**
```python
result = await lookup_term("MCP")
# Returns exact match or suggestions if term not found
```

### `batch_lookup_terms`
Look up multiple terms at once to reduce round trips.

**Parameters:**
- `terms` (list of strings): List of terms to look up

**Returns:** Dictionary mapping each term to its lookup results

**Example:**
```python
result = await batch_lookup_terms(["MCP", "API", "Protocol"])
# Returns: {"MCP": [...], "API": [...], "Protocol": [...]}
```

### `fuzzy_search_terms`
Search for terms using fuzzy matching for typos and variations.

**Parameters:**
- `query` (string): The search query
- `threshold` (integer, optional): Similarity threshold (0-100), default 80

**Returns:** List of matching terms with similarity scores

**Example:**
```python
result = await fuzzy_search_terms("mcP", 70)
# Finds "MCP" despite typo/case differences
```

### `smart_query`
AI-powered contextual search across the glossary using natural language.

**Parameters:**
- `query` (string): Natural language query describing what you're looking for
- `context` (string, optional): Additional context to help with the search

**Returns:** List of relevant terms found by AI analysis

**Example:**
```python
result = await smart_query("What is a protocol for AI models?")
# AI finds relevant terms like "MCP", "Protocol", etc.
```

### `list_terms`
List available terms in the glossary with optional filtering.

**Parameters:**
- `prefix` (string, optional): Prefix to filter terms (case-insensitive)

**Returns:** List of term names matching the filters

**Example:**
```python
result = await list_terms("M")
# Returns all terms starting with "M"
```

## Configuration

The plugin uses environment variables for configuration:

### Required Files
- `LEXY_GLOSSARY_PATH`: Path to the YAML glossary file (default: "glossary.yaml")

### AI Features (Optional)
- `LEXY_LLM_MODEL`: AI model for semantic search (default: "gemini-2.0-flash")
- `LEXY_LLM_GEMINI_API_KEY`: API key for Gemini models
- `LEXY_LLM_OPENAI_API_KEY`: API key for OpenAI models

## Glossary Format

The plugin expects a YAML file with the following structure:

```yaml
Term Name:
  definitions:
    - text: "Primary definition of the term"
      see_also: ["Related Term 1", "Related Term 2"]
    - text: "Alternative definition"
      see_also: ["Another Related Term"]

Another Term:
  definitions:
    - text: "Definition text"
      see_also: []
```

## Search Modes

### 1. Exact Search
- Case-insensitive exact matching
- Returns suggestions if no exact match found
- Fastest search method

### 2. Fuzzy Search
- Handles typos and variations
- Configurable similarity threshold
- Uses advanced string matching algorithms (rapidfuzz)

### 3. AI-Powered Search
- Natural language queries
- Contextual understanding
- Finds semantically related terms
- Requires API key for LLM access

## Dependencies

- `pydantic>=2.0.0`: Data validation and serialization
- `rapidfuzz>=3.0.0`: Fast fuzzy string matching
- `PyYAML>=6.0.0`: YAML file parsing
- `pydantic-ai` (optional): For AI-powered search features

## Error Handling

- Graceful fallback when AI features are unavailable
- Fuzzy search fallback for failed AI queries
- Empty results for missing glossary files
- Suggestion system for near-miss searches

## Performance

- Lazy initialization of search components
- Efficient batch operations
- Indexed search for fast lookups
- Configurable result limits

## Use Cases

- **Documentation Systems**: Quick lookup of technical terms
- **Knowledge Management**: Semantic search across organizational glossaries
- **Content Creation**: Find related terms and concepts
- **API Documentation**: Lookup protocol and interface definitions
- **Educational Tools**: Explore interconnected concepts

## Integration

The plugin integrates seamlessly with agentkit's tool system and can be used alongside other plugins for comprehensive knowledge management workflows.
