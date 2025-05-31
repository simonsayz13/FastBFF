import yaml
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastbff.router_builder import build_routes


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def create_app(config, env):
    startup_config = config.get("startup", {})
    host = "0.0.0.0" if env == "prod" else "127.0.0.1"
    port = startup_config.get("port", 8000)
    title = startup_config.get("title", "fastBFF")
    version = startup_config.get("version", "1.0.0")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            print(
                f"✅ {title} v{version} started successfully on http://{host}:{port}",
                flush=True,
            )
            yield
        except Exception as e:
            print(f"Startup failed: {e}", flush=True)
            sys.exit(1)

    app = FastAPI(title=title, version=version, lifespan=lifespan)
    build_routes(app, config["routes"])
    return app, host, port, startup_config.get("log_level", "error").lower()
