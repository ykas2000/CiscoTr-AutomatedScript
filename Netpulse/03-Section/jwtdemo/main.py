import os
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

app = FastAPI(
    title="NetPulse Device Security Demo",
    version="1.0.0",
    description="Training demo for JWT-protected FastAPI endpoints.",
)

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

DEMO_USERNAME = os.getenv("DEMO_USERNAME")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")

if not DEMO_USERNAME or not DEMO_PASSWORD or not JWT_SECRET:
    raise RuntimeError(
        "Set DEMO_USERNAME, DEMO_PASSWORD and JWT_SECRET environment variables before starting the app."
    )

password_hash = PasswordHash.recommended()
demo_user = {
    "username": DEMO_USERNAME,
    "password_hash": password_hash.hash(DEMO_PASSWORD),
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class DeviceStatusUpdate(BaseModel):
    status: Literal["online", "offline", "maintenance"]


devices = {
    1: {"id": 1, "name": "Router-01", "status": "online"},
    2: {"id": 2, "name": "Switch-01", "status": "offline"},
}


def authenticate(username: str, password: str) -> bool:
    return (
        username == demo_user["username"]
        and password_hash.verify(password, demo_user["password_hash"])
    )


def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    payload = {"sub": subject, "exp": expires}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != demo_user["username"]:
            raise credentials_error
        return str(username)
    except InvalidTokenError:
        raise credentials_error


@app.get("/")
def home():
    return {"message": "Security demo API is running"}


@app.get("/devices")
def list_devices():
    return list(devices.values())


@app.post("/auth/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    if not authenticate(form.username, form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(form.username),
        "token_type": "bearer",
    }


@app.patch("/devices/{device_id}/status")
def update_device_status(
    device_id: int,
    payload: DeviceStatusUpdate,
    current_user: str = Depends(get_current_user),
):
    device = devices.get(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    device["status"] = payload.status
    return {
        "updated_by": current_user,
        "device": device,
    }
