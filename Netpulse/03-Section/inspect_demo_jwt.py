#!/usr/bin/env python3
import os
import sys
import jwt

if len(sys.argv) != 2:
    print("Usage: python inspect_demo_jwt.py '<TOKEN>'")
    sys.exit(2)

secret = os.getenv("JWT_SECRET")
if not secret:
    print("JWT_SECRET is not set.")
    sys.exit(2)

token = sys.argv[1]
claims = jwt.decode(token, secret, algorithms=["HS256"])

print("Safe JWT claim inspection")
print(f"sub: {claims.get('sub')}")
print(f"exp: {claims.get('exp')}")
