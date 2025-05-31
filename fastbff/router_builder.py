from fastapi import APIRouter, Depends
from fastbff.http_handlers import static_handler, proxy_handler, echo_handler
from fastbff.middlewares.rate_limiter import rate_limiter
from fastbff.middlewares.authentication import authentication


def build_routes(app, routes):
    router = APIRouter()

    for route in routes:
        path = route["path"]
        method = route["method"].upper()
        source = route["source"]
        source_type = source["type"]
        rate_limit: bool = route.get("limit_rate", False)
        auth = route.get("auth", False)
        dependencies = []

        if auth:
            auth_token = route.get("auth_token", True)
            dependencies.append(Depends(authentication(auth_token)))
        if rate_limit:
            rate_limit_count: int = route.get("limit_count", 0)
            rate_limit_window: int = route.get("limit_window", 0)
            dependencies.append(
                Depends(rate_limiter(rate_limit_count, rate_limit_window))
            )

        # Static
        if source_type == "static":
            handler = static_handler(source["data"])
            router.add_api_route(
                path, handler, methods=[method], dependencies=dependencies
            )

        # Proxy
        elif source_type == "proxy":
            handler = proxy_handler(source["url"])
            router.add_api_route(
                path, handler, methods=[method], dependencies=dependencies
            )

        # Echo
        elif source_type == "echo" and method == "POST":
            router.add_api_route(
                path, echo_handler, methods=["POST"], dependencies=dependencies
            )

    app.include_router(router)
