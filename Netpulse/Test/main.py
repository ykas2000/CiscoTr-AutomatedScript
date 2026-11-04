# main.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="Device Management Test API")

# In-memory mock database matching our test scenarios
devices_db = [
    {"id": 101, "hostname": "edge-01", "status": "online"}
]

alerts_db = [
    {"id": 1, "message": "High CPU usage on gateway"}
]

class DevicePayload(BaseModel):
    hostname: str
    status: str

@app.get("/devices")
def get_devices(authorization: str | None = Header(default=None)):
    """
    Protected endpoint: Requires a Bearer token in headers 
    to support Authentication Exercises (5 & 6).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid token")
    return devices_db

@app.get("/devices/{device_id}")
def get_device_by_id(device_id: int):
    """
    Positive/Negative test endpoint: Returns 200 if found, 404 if missing.
    """
    for device in devices_db:
        if device["id"] == device_id:
            return device
    raise HTTPException(status_code=404, detail="Device not found")

@app.post("/devices", status_code=201)
def create_device(payload: DevicePayload):
    """
    POST endpoint: Creates a new device and returns 201 Created.
    """
    new_device = {
        "id": len(devices_db) + 101,
        "hostname": payload.hostname,
        "status": payload.status
    }
    devices_db.append(new_device)
    return new_device

@app.get("/alerts")
def get_alerts():
    """
    Alerts endpoint for multi-file test suite organization.
    """
    return alerts_db