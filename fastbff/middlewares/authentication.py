from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token: str = ""):
        super().__init__(app)
        self.auth_token = token

    async def dispatch(self, request: Request, next):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Authorization required"}, status_code=401)

        incoming_token = auth_header.split("Bearer ")[-1]

        if incoming_token != self.auth_token:
            return JSONResponse({"error": "Invalid token"}, status_code=401)

        return await next(request)
