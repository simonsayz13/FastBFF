from fastapi import HTTPException, Request


def authentication(expected_token: str):
    async def verify_token(request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        token = auth_header.split("Bearer ")[1]
        if token != expected_token:
            raise HTTPException(status_code=403, detail="Unauthorized")

    return verify_token
