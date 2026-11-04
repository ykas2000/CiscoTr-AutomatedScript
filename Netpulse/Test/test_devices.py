import httpx

BASE_URL = "http://localhost:8000"

def test_get_devices():
    url = f"{BASE_URL}/devices"
    headers = {"Authorization": "Bearer test-token-123"}
    
    print("\n--- Exercise 1: Basic GET Request ---")
    print(f"👉 Sending GET request to: {url}")
    
    response = httpx.get(url, headers=headers)
    print(f"📥 Received Status Code: {response.status_code}")
    
    assert response.status_code == 200
    print("✅ Status code 200 OK verified!")