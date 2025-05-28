#!/usr/bin/env python3
"""
Test script for Google Web Search plugin
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add the plugin directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from search_web import search_web

def test_search():
    """Test the web search functionality."""
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_WEBSEARCH_API_KEY")
    if not api_key:
        print("❌ GOOGLE_WEBSEARCH_API_KEY not set in environment")
        print("Please set your Gemini API key in the .env file")
        return False
    
    print("🔍 Testing Google Web Search plugin...")
    print(f"API Key: {'*' * (len(api_key) - 4) + api_key[-4:]}")
    
    # Test search
    test_query = "Cheat Codes for Zelda Minish Cap"
    print(f"Query: {test_query}")
    
    try:
        result = search_web(test_query)
        
        if result["status"] == "success":
            print("✅ Search successful!")
            data = result["data"]
            print(f"Response length: {len(data['response'])} characters")
            print(f"References found: {data['reference_count']}")
            print(f"Search queries used: {data['search_queries']}")
            
            print("Response:")
            print(data["response"])

            # Show first few references
            if data["references"]:
                print("\n📚 First few references:")
                for i, ref in enumerate(data["references"][:3]):
                    print(f"  {i+1}. {ref['title']}")
                    print(f"     URL: {ref['url']}")
                    if ref.get('confidence'):
                        print(f"     Confidence: {ref['confidence']:.2f}")
                    print()
            
            return True
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during search: {e}")
        return False

if __name__ == "__main__":
    success = test_search()
    sys.exit(0 if success else 1) 