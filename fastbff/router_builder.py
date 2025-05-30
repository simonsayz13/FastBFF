from fastapi import APIRouter
from fastbff.http_handlers import static_handler, proxy_handler, echo_handler
from fastbff.middlewares.rate_limiter import RateLimiterMiddleware
from fastbff.middlewares.authentication import AuthMiddleware


def build_routes(app, routes):
    router = APIRouter()

    for route in routes:
        path = route["path"]
        method = route["method"].upper()
        source = route["source"]
        source_type = source["type"]
        rate_limit: bool = route.get("limit_rate", False)
        rate_limit_count: int = route.get("limit_count", 0)
        rate_limit_window: int = route.get("limit_window", 0)
        auth = route.get("auth", False)
        auth_token = route.get("auth_token", True)

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

        # rate limiter
        if rate_limit:
            app.add_middleware(
                RateLimiterMiddleware,
                max_requests=rate_limit_count,
                window_seconds=rate_limit_window,
            )

        # auth token
        if auth:
            app.add_middleware(AuthMiddleware, token=auth_token)

    app.include_router(router)
