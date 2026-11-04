import httpx

BASE_URL = "http://localhost:8000"

def test_get_devices_missing_token():
    response = httpx.get(f"{BASE_URL}/devices")
    assert response.status_code == 401