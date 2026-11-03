# API Security Review

PASS — Password is not stored as plaintext in source code.
PASS — JWT signing secret is read from an environment variable.
PASS — JWT contains an expiry claim.
PASS — Protected route requires a bearer token.
PASS — No token is rejected.
PASS — Invalid token is rejected.
PASS — Valid token succeeds.
PASS — HTTPS is required before using bearer tokens outside this local lab.
PASS — Authentication does not replace authorization.
PASS — JWT does not solve every OWASP API risk.
