import httpx

BASE_URL = "http://localhost:8000"

def test_get_alerts():
    url = f"{BASE_URL}/alerts"
    
    print("\n--- Exercise 7: Alerts Suite Endpoint ---")
    print(f"👉 Fetching system alerts from: {url}")
    
    response = httpx.get(url)
    print(f"📥 Received Status Code: {response.status_code}")
    
    assert response.status_code == 200
    data = response.json()
    print(f"📦 Alerts List: {data}")
    
    assert isinstance(data, list)
    assert len(data) > 0
    print("✅ Alerts test completed successfully!")