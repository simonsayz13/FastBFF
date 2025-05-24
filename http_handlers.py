from fastapi import Request
from fastapi.responses import JSONResponse
import httpx

def static_handler(data):
    async def handler():
        return JSONResponse(content=data)
    return handler

def proxy_handler(url):
    async def handler():
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return JSONResponse(content=response.json())
    return handler

async def echo_handler(request: Request):
    body = await request.json()
    return JSONResponse(content={"received": body})