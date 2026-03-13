import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health...")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
        print("PASS: Health check passed")
    except Exception as e:
        print(f"FAIL: Health check failed: {e}")
        return False
    return True

def test_tools():
    print("Testing /tools...")
    try:
        resp = requests.get(f"{BASE_URL}/tools")
        assert resp.status_code == 200
        tools = [t["name"] for t in resp.json()["tools"]]
        required = ["memory_write", "memory_read", "memory_retrieve_by_context"]
        for r in required:
            assert r in tools
        print("PASS: Tools list passed")
    except Exception as e:
        print(f"FAIL: Tools list failed: {e}")
        return False
    return True

def test_memory_write():
    print("Testing /invoke/memory_write...")
    try:
        payload = {
            "memory_type": "conversation",
            "data": {
                "user_id": "test_user_01",
                "turn_id": 1,
                "role": "user",
                "content": "I want to learn about computer graphics."
            }
        }
        resp = requests.post(f"{BASE_URL}/invoke/memory_write", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "success"
        assert "memory_id" in data
        print(f"PASS: Memory write passed (ID: {data['memory_id']})")
        return data["memory_id"]
    except Exception as e:
        print(f"FAIL: Memory write failed: {e}")
        return None

def test_memory_read():
    print("Testing /invoke/memory_read...")
    try:
        payload = {
            "user_id": "test_user_01",
            "query_type": "last_n_turns",
            "params": {"n": 5}
        }
        resp = requests.post(f"{BASE_URL}/invoke/memory_read", json=payload)
        assert resp.status_code == 200
        results = resp.json()["results"]
        assert len(results) > 0
        assert results[0]["content"] == "I want to learn about computer graphics."
        print("PASS: Memory read passed")
    except Exception as e:
        print(f"FAIL: Memory read failed: {e}")
        return False
    return True

def test_semantic_search():
    print("Testing /invoke/memory_retrieve_by_context...")
    try:
        # First write some context
        requests.post(f"{BASE_URL}/invoke/memory_write", json={
            "memory_type": "conversation",
            "data": {
                "user_id": "test_user_02",
                "turn_id": 1,
                "role": "user",
                "content": "The student mentioned an interest in quantum physics."
            }
        })
        
        payload = {
            "user_id": "test_user_02",
            "query_text": "What subjects does the student find interesting?",
            "top_k": 1
        }
        resp = requests.post(f"{BASE_URL}/invoke/memory_retrieve_by_context", json=payload)
        assert resp.status_code == 200
        results = resp.json()["results"]
        assert len(results) > 0
        assert "quantum physics" in results[0]["content"]
        assert "score" in results[0]
        print(f"PASS: Semantic search passed (Score: {results[0]['score']})")
    except Exception as e:
        print(f"FAIL: Semantic search failed: {e}")
        return False
    return True

if __name__ == "__main__":
    # Wait for server to be ready
    max_retries = 30
    ready = False
    for i in range(max_retries):
        try:
            requests.get(f"{BASE_URL}/health")
            ready = True
            break
        except:
            print(f"Waiting for server... ({i+1}/{max_retries})")
            time.sleep(5)
    
    if not ready:
        print("Server failed to start")
        sys.exit(1)
        
    all_passed = True
    all_passed &= test_health()
    all_passed &= test_tools()
    mem_id = test_memory_write()
    all_passed &= (mem_id is not None)
    all_passed &= test_memory_read()
    all_passed &= test_semantic_search()
    
    if all_passed:
        print("\nALL TESTS PASSED!")
    else:
        print("\nSOME TESTS FAILED!")
        sys.exit(1)
