import time
from fastapi import HTTPException, Request

ip_timestamps = {}


def rate_limiter(max_requests: int, window_seconds: int):
    async def limiter(request: Request):
        ip = request.client.host
        now = time.time()
        request_times = ip_timestamps.get(ip, [])
        request_times = [t for t in request_times if now - t < window_seconds]
        if len(request_times) >= max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        request_times.append(now)
        ip_timestamps[ip] = request_times

    return limiter
