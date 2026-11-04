import httpx

BASE_URL = "http://localhost:8000"

def test_devices_json_structure():
    url = f"{BASE_URL}/devices"
    headers = {"Authorization": "Bearer test-token-123"}
    
    print("\n--- Exercise 5: Validating JSON Structure ---")
    print(f"👉 Fetching devices for structure verification...")
    
    response = httpx.get(url, headers=headers)
    print(f"📥 Status Code: {response.status_code}")
    assert response.status_code == 200
    
    data = response.json()
    print(f"📦 Full Response Data: {data}")
    
    print("🔍 Validating JSON data types...")
    assert isinstance(data, list)
    assert len(data) > 0
    
    first_device = data[0]
    print(f"🔍 First item attributes: ID={first_device.get('id')}, Hostname={first_device.get('hostname')}")
    assert "hostname" in first_device
    assert "status" in first_device
    print("✅ JSON structure matches expected schema!")