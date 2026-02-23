"""
Test Script for Panaversity RAG Chatbot API
Run this after starting the backend to verify all endpoints work correctly.

Usage:
    python test_api.py
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30  # seconds

def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_result(test_name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {test_name}")
    if details:
        print(f"   {details}")

def test_health():
    """Test health check endpoint."""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        passed = (
            data.get("status") in ["healthy", "degraded"] and
            data.get("qdrant") == "connected"
        )
        
        print_result(
            "Health endpoint responds",
            passed,
            f"Status: {data.get('status')}, Qdrant: {data.get('qdrant')}, Gemini: {data.get('gemini')}"
        )
        
        return passed
    except Exception as e:
        print_result("Health endpoint responds", False, str(e))
        return False

def test_root():
    """Test root endpoint."""
    print_section("TEST 2: Root Endpoint")
    
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        passed = (
            data.get("name") == "Panaversity RAG Chatbot API" and
            "endpoints" in data
        )
        
        print_result(
            "Root endpoint responds",
            passed,
            f"API: {data.get('name')}, Version: {data.get('version')}"
        )
        
        return passed
    except Exception as e:
        print_result("Root endpoint responds", False, str(e))
        return False

def test_chat_basic():
    """Test basic chat endpoint."""
    print_section("TEST 3: Basic Chat")
    
    try:
        payload = {
            "query": "What is humanoid robotics?",
            "session_id": "test_session",
            "language": "en"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        passed = (
            "response" in data and
            "sources" in data and
            "duration_ms" in data
        )
        
        print_result(
            "Chat endpoint responds",
            passed,
            f"Response length: {len(data.get('response', ''))} chars, "
            f"Sources: {len(data.get('sources', []))}, "
            f"Duration: {data.get('duration_ms')}ms"
        )
        
        if passed:
            print(f"\n   Sample response (first 100 chars):")
            print(f"   \"{data['response'][:100]}...\"")
        
        return passed
    except Exception as e:
        print_result("Chat endpoint responds", False, str(e))
        return False

def test_chat_with_selection():
    """Test chat with selected text endpoint."""
    print_section("TEST 4: Chat with Selected Text")
    
    try:
        payload = {
            "query": "Explain this concept",
            "selected_text": "A transformation matrix represents the relationship between coordinate frames.",
            "session_id": "test_session",
            "language": "en"
        }
        
        response = requests.post(
            f"{BASE_URL}/ask-with-selection",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        passed = (
            "response" in data and
            data.get("has_selection") == True
        )
        
        print_result(
            "Ask-with-selection endpoint responds",
            passed,
            f"Response length: {len(data.get('response', ''))} chars, "
            f"Has selection: {data.get('has_selection')}"
        )
        
        return passed
    except Exception as e:
        print_result("Ask-with-selection endpoint responds", False, str(e))
        return False

def test_chat_urdu():
    """Test Urdu language support."""
    print_section("TEST 5: Urdu Language Support")
    
    try:
        payload = {
            "query": "humanoid robotics کیا ہے؟",
            "session_id": "test_session",
            "language": "ur"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        passed = (
            "response" in data and
            data.get("language") == "ur"
        )
        
        print_result(
            "Urdu chat works",
            passed,
            f"Language: {data.get('language')}, "
            f"Response length: {len(data.get('response', ''))} chars"
        )
        
        if passed:
            print(f"\n   Urdu response (first 100 chars):")
            print(f"   \"{data['response'][:100]}...\"")
        
        return passed
    except Exception as e:
        print_result("Urdu chat works", False, str(e))
        return False

def test_stats():
    """Test stats endpoint."""
    print_section("TEST 6: Knowledge Base Stats")
    
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        passed = (
            "collection_name" in data and
            "vectors_count" in data
        )
        
        print_result(
            "Stats endpoint responds",
            passed,
            f"Collection: {data.get('collection_name')}, "
            f"Vectors: {data.get('vectors_count')}"
        )
        
        return passed
    except Exception as e:
        print_result("Stats endpoint responds", False, str(e))
        return False

def test_clear_history():
    """Test clear history endpoint."""
    print_section("TEST 7: Clear History")
    
    try:
        response = requests.post(
            f"{BASE_URL}/clear-history",
            params={"session_id": "test_session"},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        passed = data.get("status") == "success"
        
        print_result(
            "Clear history works",
            passed,
            f"Message: {data.get('message')}"
        )
        
        return passed
    except Exception as e:
        print_result("Clear history works", False, str(e))
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║     PANAVERSITY RAG CHATBOT - API TEST SUITE          ║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    print(f"\nTesting backend at: {BASE_URL}")
    print(f"Timeout: {TIMEOUT}s per request\n")
    
    # Check if backend is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Backend is not running!")
        print(f"   Please start the backend: python main.py")
        print(f"   at {BASE_URL}\n")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Basic Chat", test_chat_basic),
        ("Chat with Selection", test_chat_with_selection),
        ("Urdu Support", test_chat_urdu),
        ("Knowledge Base Stats", test_stats),
        ("Clear History", test_clear_history),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'=' * 60}\n")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot is working correctly.\n")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
