import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, next):
        time_now = time.time()
        identifier = (request.client.host, request.url.path)
        request_times = self.requests.get(identifier, [])

        # Filter requests times
        request_times = [t for t in request_times if time_now - t < self.window_seconds]

        if len(request_times) >= self.max_requests:
            return JSONResponse(
                {"error": "Rate limit exceeded. Try again later."}, status_code=429
            )

        # Log this request
        request_times.append(time_now)
        self.requests[identifier] = request_times

        response = await next(request)
        return response
