import httpx

BASE_URL = "http://localhost:8000"

def test_get_device_positive():
    """
    Positive Test: Requesting a valid, existing device ID.
    Expected: Status code 200 OK and matching resource data.
    """
    device_id = 101
    url = f"{BASE_URL}/devices/{device_id}"
    
    print("\n--- Positive Test: Fetching Existing Device ---")
    print(f"👉 Sending GET request to: {url}")
    
    response = httpx.get(url)
    print(f"📥 Received Status Code: {response.status_code}")
    
    assert response.status_code == 200
    
    data = response.json()
    print(f"📦 Response Payload: {data}")
    assert data["id"] == device_id
    print("✅ Positive test passed successfully!")


def test_get_device_negative():
    """
    Negative Test: Requesting a non-existent device ID.
    Expected: Status code 404 Not Found (controlled failure/error response).
    """
    missing_id = 99999
    url = f"{BASE_URL}/devices/{missing_id}"
    
    print("\n--- Negative Test: Fetching Missing Device ---")
    print(f"👉 Sending GET request for non-existent ID: {missing_id} at {url}")
    
    response = httpx.get(url)
    print(f"📥 Received Status Code: {response.status_code}")
    
    assert response.status_code == 404
    
    error_detail = response.json()
    print(f"🔍 Server Error Message: {error_detail}")
    assert "detail" in error_detail
    print("✅ Negative test passed (Expected 404 received correctly)!")