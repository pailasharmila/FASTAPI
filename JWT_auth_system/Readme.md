Built a Secure JWT Auth System:
First Try to understand what is JWT from here ---->https://www.geeksforgeeks.org/web-tech/json-web-token-jwt/

later on I started executing this : https://medium.com/@hadiyolworld007/how-i-built-a-secure-jwt-auth-system-in-just-20-minutes-0d2ae5d0a5ad

The Stack
🐍 Python 3.11+
⚡ FastAPI
🔑 python-jose for JWT signing/verification
🔒 passlib for password hashing


Most Common JWT vulnerabilites & exploitations
- https://www.vaadata.com/en/blog/jwt-json-web-token-vulnerabilities-common-attacks-and-security-best-practices/#what-are-the-most-common-jwt-vulnerabilities-and-exploitations
- the jwt.io site to easily view and manipulate tokens
- check the case where algo=none & weak jwt secret
