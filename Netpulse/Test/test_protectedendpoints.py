import httpx

BASE_URL = "http://localhost:8000"

def test_protected_devices_endpoint():
    url = f"{BASE_URL}/devices"
    
    print("\n--- Exercise 6: Authorization Header Check ---")
    
    # 1. Attempt unauthenticated access
    print("👉 Test 6a: Attempting access WITHOUT Bearer token...")
    unauth_response = httpx.get(url)
    print(f"📥 Status Code (No Token): {unauth_response.status_code}")
    assert unauth_response.status_code == 401
    print("✅ Correctly rejected with 401 Unauthorized!")
    
    # 2. Attempt authenticated access
    print("👉 Test 6b: Attempting access WITH Bearer token...")
    headers = {"Authorization": "Bearer test-token-123"}
    auth_response = httpx.get(url, headers=headers)
    print(f"📥 Status Code (With Token): {auth_response.status_code}")
    assert auth_response.status_code == 200
    print(f"📦 Authenticated Payload: {auth_response.json()}")
    print("✅ Protected access granted!")