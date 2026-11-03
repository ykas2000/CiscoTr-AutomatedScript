#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

import httpx
import jwt

BASE = "http://127.0.0.1:8000"
USERNAME = os.getenv("DEMO_USERNAME")
PASSWORD = os.getenv("DEMO_PASSWORD")
SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

if not USERNAME or not PASSWORD or not SECRET:
    print("[FAIL] Required training environment variables are not set.")
    sys.exit(2)

passed = 0
failed = 0

def check(label, condition, detail=""):
    global passed, failed
    if condition:
        print(f"[PASS] {label} {detail}")
        passed += 1
    else:
        print(f"[FAIL] {label} {detail}")
        failed += 1

with httpx.Client(base_url=BASE, timeout=5.0) as client:
    r = client.get("/devices")
    check("Public GET /devices", r.status_code == 200, f"HTTP {r.status_code}")

    r = client.patch("/devices/1/status", json={"status": "maintenance"})
    check("No token -> 401", r.status_code == 401, f"HTTP {r.status_code}")

    r = client.patch(
        "/devices/1/status",
        json={"status": "maintenance"},
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    check("Invalid token -> 401", r.status_code == 401, f"HTTP {r.status_code}")

    r = client.post(
        "/auth/token",
        data={"username": USERNAME, "password": "wrong-password"},
    )
    check("Invalid login -> 401", r.status_code == 401, f"HTTP {r.status_code}")

    r = client.post(
        "/auth/token",
        data={"username": USERNAME, "password": PASSWORD},
    )
    token = None
    if r.status_code == 200:
        token = r.json().get("access_token")
    check(
        "Valid login -> bearer token",
        r.status_code == 200 and bool(token) and r.json().get("token_type") == "bearer",
        f"HTTP {r.status_code}",
    )

    if token:
        claims = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        check("JWT subject claim", claims.get("sub") == USERNAME, f"sub={claims.get('sub')}")
        exp = claims.get("exp")
        now = int(datetime.now(timezone.utc).timestamp())
        check("JWT expiry claim", isinstance(exp, int) and exp > now, f"exp={exp}")

        headers = {"Authorization": f"Bearer {token}"}
        r = client.patch(
            "/devices/1/status",
            json={"status": "maintenance"},
            headers=headers,
        )
        body = r.json() if r.content else {}
        check(
            "Valid token PATCH -> 200",
            r.status_code == 200
            and body.get("device", {}).get("status") == "maintenance"
            and body.get("updated_by") == USERNAME,
            f"HTTP {r.status_code}",
        )

        r = client.get("/devices")
        statuses = {d["id"]: d["status"] for d in r.json()} if r.status_code == 200 else {}
        check(
            "State change observable",
            r.status_code == 200 and statuses.get(1) == "maintenance",
            f"HTTP {r.status_code}",
        )

        r = client.patch(
            "/devices/999/status",
            json={"status": "offline"},
            headers=headers,
        )
        check("Missing device with valid token -> 404", r.status_code == 404, f"HTTP {r.status_code}")

print(f"\nPassed: {passed}  Failed: {failed}")
if failed:
    print("RESULT: FAIL")
    sys.exit(1)

print("RESULT: PASS")
