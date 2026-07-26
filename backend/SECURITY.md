# Security Policy

## Supported Versions
Only the latest major version of IntelliBuild AI receives security patches.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within IntelliBuild AI, please send an e-mail to `engineering@intellibuild.ai`. All security vulnerabilities will be promptly addressed.

## Secure Development Principles
- **No Secrets in Code**: Never commit API keys, database passwords, or JWT secrets. Use `.env` files.
- **Input Validation**: All incoming external data must be validated via Pydantic v2 schemas.
- **Dependency Scanning**: Dependencies are scanned during CI for known CVEs.
