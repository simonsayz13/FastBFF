from fastapi import FastAPI
import yaml
import uvicorn
from router_builder import build_routes
from contextlib import asynccontextmanager
import sys

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

startup_config = config.get("startup", {})
host = startup_config.get("host", "127.0.0.1")
port = startup_config.get("port", 8000)
log_level = startup_config.get("log_level", "error").lower()
title = startup_config.get("title", "fastBFF")
version = startup_config.get("version", "1.0.0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(
            f"{title} v{version} started successfully on http://{host}:{port}",
            flush=True,
        )
        yield  # This is where the app starts running
    except Exception as e:
        print(f"Startup failed: {e}", flush=True)
        sys.exit(1)


app = FastAPI(title=title, version=version, lifespan=lifespan)

build_routes(app, config["routes"])

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port, log_level="error")
