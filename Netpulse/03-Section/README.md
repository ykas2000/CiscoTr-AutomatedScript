# M2S3 Demo 01 — JWT Authentication for FastAPI

Trainer demo source, aligned with the Simplilearn screenshots. The demo uses an in-memory device list and one protected PATCH endpoint.

## Ubuntu / Simplilearn Sandbox setup

1. Extract this ZIP. In VS Code open the extracted `security/jwt-demo` folder (it contains `main.py`).
2. Open a terminal in `security/jwt-demo`. Create and activate a virtual environment if the supplied lab environment is not already configured:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Set LAB-ONLY credentials in the same terminal before starting Uvicorn. Replace the values; do not publish them or take screenshots of the real values.

```bash
export DEMO_USERNAME=operator
export DEMO_PASSWORD='choose-a-demo-password'
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Note: keep that terminal running. This is for a local training environment, not production security architecture.

4. Open `http://127.0.0.1:8000/docs`. Verify `GET /devices` is public. Without authorization, `PATCH /devices/1/status` returns 401.
5. In Swagger, use `POST /auth/token` with **application/x-www-form-urlencoded**, using the exact username/password above; alternatively use Swagger's **Authorize** OAuth2 dialog. Do not send JSON to this endpoint.
6. Copy the bearer access token into the Swagger **Authorize** dialog (or set Postman Authorization → Bearer Token). PATCH `/devices/1/status` using `{"status":"maintenance"}`; expect HTTP 200. GET `/devices` again to confirm the status changed.
7. In a second terminal, activate the same environment, export the same DEMO_USERNAME, DEMO_PASSWORD and JWT_SECRET values and run the validation script from the `security` folder:

```bash
python validate_m2s3_demo.py
```

The validator executes 10 checks. `inspect_demo_jwt.py` is an optional claims viewer; it prints only `sub` and `exp`. Never share full bearer tokens, plaintext passwords, or signing secrets.

## Endpoints
- `GET /` → 200
- `GET /devices` → 200 (public)
- `POST /auth/token` → 200 valid login, 401 invalid credentials (form fields, not JSON)
- `PATCH /devices/{device_id}/status` → 401 missing/invalid token, 200 valid token, 404 missing device

The demo intentionally **does not implement user roles or per-device authorization**. Authentication confirms the demo user; authorization is a separate concept. Use HTTPS for anything outside the isolated local lab.
