# Google Web Search Plugin

A powerful web search plugin powered by Google's Gemini API with grounding support. This plugin provides real-time web search capabilities with citation extraction and rate limiting to work within free API quotas.

## Features

- 🔍 **Real-time web search** using Google Gemini API with grounding
- 📚 **Citation extraction** with URL following and title extraction
- ⚡ **Rate limiting** with exponential backoff using Tenacity
- 🛡️ **Error handling** for API limits and network issues
- 🔧 **Configurable** via environment variables
- 📊 **Detailed results** with confidence scores and metadata

## Installation

1. Install the required dependencies:
```bash
pip install -r plugin_requirements.txt
```

2. Set up your environment variables in `.env`:
```bash
# Required
GOOGLE_WEBSEARCH_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
GOOGLE_WEBSEARCH_ENABLED=true
GOOGLE_WEBSEARCH_MODEL=gemini-2.0-flash
GOOGLE_WEBSEARCH_MAX_REFERENCES=10
GOOGLE_WEBSEARCH_TIMEOUT=10
```

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the API key to your `.env` file

## Usage

### Basic Search
```python
from plugins.google_websearch.search_web import search_web

result = search_web("latest developments in AI")

if result["status"] == "success":
    data = result["data"]
    print(f"Response: {data['response']}")
    print(f"References: {len(data['references'])}")
    
    for ref in data["references"]:
        print(f"- {ref['title']}: {ref['url']}")
```

### Response Format
```json
{
  "status": "success",
  "data": {
    "query": "your search query",
    "search_queries": ["actual queries used by Gemini"],
    "response": "AI-generated response with grounding",
    "references": [
      {
        "content": "relevant text snippet",
        "url": "https://example.com",
        "title": "Page Title",
        "confidence": 0.95
      }
    ],
    "reference_count": 5
  }
}
```

## Configuration

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| `GOOGLE_WEBSEARCH_API_KEY` | Gemini API key | - | ✅ |
| `GOOGLE_WEBSEARCH_ENABLED` | Enable/disable plugin | `true` | ❌ |
| `GOOGLE_WEBSEARCH_MODEL` | Gemini model to use | `gemini-2.0-flash` | ❌ |
| `GOOGLE_WEBSEARCH_MAX_REFERENCES` | Max references to return | `10` | ❌ |
| `GOOGLE_WEBSEARCH_TIMEOUT` | Request timeout (seconds) | `10` | ❌ |

## Rate Limiting

The plugin includes built-in rate limiting to work with free Gemini API quotas:

- **Retry Logic**: Up to 3 attempts with exponential backoff
- **Rate Limit Detection**: Automatically detects and handles 429 errors
- **Backoff Strategy**: 4-10 second delays between retries
- **Free Tier Friendly**: Designed to work within 15 requests/minute limit

## Testing

Run the test script to verify your setup:

```bash
cd plugins/google_websearch
python test_search.py
```

## Error Handling

The plugin handles various error conditions:

- **Missing API Key**: Returns error with setup instructions
- **Rate Limits**: Automatic retry with exponential backoff
- **Network Issues**: Graceful degradation with error messages
- **Invalid Responses**: Robust parsing with fallbacks

## Dependencies

- `google-genai>=0.3.0` - Google Gemini API client
- `tenacity>=8.0.0` - Retry logic with exponential backoff
- `requests>=2.25.0` - HTTP requests for URL following
- `aiohttp>=3.8.0` - Async HTTP support

## License

This plugin is part of the AgentKit project and follows the same license terms. 