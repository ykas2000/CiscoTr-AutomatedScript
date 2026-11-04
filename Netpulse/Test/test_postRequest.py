import httpx

def test_create_device():
    BASE_URL = "http://localhost:8000"
    url = f"{BASE_URL}/devices"
    payload = {
        "hostname": "switch-core-01",
        "status": "online"
    }
    
    print("\n--- Exercise 4: Create Device (POST) ---")
    print(f"👉 Sending POST payload: {payload}")
    
    response = httpx.post(url, json=payload)
    print(f"📥 Received Status Code: {response.status_code}")
    
    assert response.status_code == 201
    data = response.json()
    print(f"📦 Created Resource: {data}")
    assert data["hostname"] == "switch-core-01"
    print("✅ Resource created successfully with 201 Created!")