#!/usr/bin/env python
"""
Simple API test script to verify backend is working.
Run this after starting the backend server.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    """Test basic health check endpoint."""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_statistics():
    """Test statistics endpoint."""
    print_section("2. System Statistics")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total Requests: {data.get('total_requests', 0)}")
        print(f"Pending Requests: {data.get('pending_requests', 0)}")
        print(f"Knowledge Base Size: {data.get('knowledge_base_size', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base endpoint."""
    print_section("3. Knowledge Base")
    try:
        response = requests.get(f"{BASE_URL}/api/knowledge/all")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Knowledge Entries: {data.get('count', 0)}")
        if data.get('knowledge'):
            print("\nSample entries:")
            for entry in data['knowledge'][:3]:
                print(f"  - {entry.get('question', 'N/A')[:60]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simulate_call():
    """Test call simulation endpoint."""
    print_section("4. Simulate Call")
    try:
        payload = {
            "customer_id": "TEST_001",
            "customer_phone": "(555) 999-8888",
            "customer_name": "Test User",
            "question": "What are your hours?"
        }
        print(f"Sending: {payload['question']}")
        response = requests.post(
            f"{BASE_URL}/api/calls/simulate",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"\nAI Response: {data.get('response', 'N/A')}")
        print(f"Needs Help: {data.get('needs_help', False)}")
        if data.get('help_request_id'):
            print(f"Help Request ID: {data['help_request_id']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_escalation():
    """Test escalation by asking unknown question."""
    print_section("5. Test Escalation")
    try:
        payload = {
            "customer_id": "TEST_002",
            "customer_phone": "(555) 888-7777",
            "customer_name": "Test User 2",
            "question": "Do you offer underwater basket weaving classes?"
        }
        print(f"Sending: {payload['question']}")
        response = requests.post(
            f"{BASE_URL}/api/calls/simulate",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"\nAI Response: {data.get('response', 'N/A')}")
        print(f"Needs Help: {data.get('needs_help', False)}")
        if data.get('needs_help'):
            print("✅ Successfully escalated!")
            print(f"Help Request ID: {data.get('help_request_id', 'N/A')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pending_requests():
    """Test pending requests endpoint."""
    print_section("6. Pending Requests")
    try:
        response = requests.get(f"{BASE_URL}/api/requests/pending")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Pending Requests: {data.get('count', 0)}")
        if data.get('requests'):
            print("\nPending questions:")
            for req in data['requests'][:5]:
                print(f"  - {req.get('question', 'N/A')[:60]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "🧪 API TEST SUITE".center(60, "="))
    print("Testing Frontdesk AI Receptionist Backend")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Statistics", test_statistics),
        ("Knowledge Base", test_knowledge_base),
        ("Call Simulation", test_simulate_call),
        ("Escalation", test_escalation),
        ("Pending Requests", test_pending_requests),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append((name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
