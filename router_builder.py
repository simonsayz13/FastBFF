from fastapi import APIRouter, Request
from http_handlers import static_handler, proxy_handler, echo_handler

def build_routes(app, routes):
    router = APIRouter()

    for route in routes:
        path = route["path"]
        method = route["method"].upper()
        source = route["source"]
        source_type = source["type"]

        # Static
        if source_type == "static":
            handler = static_handler(source["data"])
            router.add_api_route(path, handler, methods=[method])

        # Proxy
        elif source_type == "proxy":
            handler = proxy_handler(source["url"])
            router.add_api_route(path, handler, methods=[method])

        # Echo
        elif source_type == "echo" and method == "POST":
            router.add_api_route(path, echo_handler, methods=["POST"])

    app.include_router(router)