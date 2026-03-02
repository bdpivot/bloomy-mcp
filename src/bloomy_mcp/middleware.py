"""Authentication middleware for the MCP HTTP server.

Validates API key on incoming requests when running in streamable-http transport mode.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Validates X-API-Key header on requests to the /mcp endpoint."""

    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/mcp"):
            provided_key = request.headers.get("x-api-key")
            if provided_key != self.api_key:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)
