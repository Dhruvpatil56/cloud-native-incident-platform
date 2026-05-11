import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from audit.audit_logger import audit_event

logger = logging.getLogger("platform-auth")


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        api_key = request.headers.get("x-api-key")
        actor = request.headers.get("x-actor", "unknown")

        logger.info("platform api request", extra={"path": request.url.path, "actor": actor})

        if not api_key or api_key != "platform-api-key":
            audit_event("api.auth.failed", actor)
            return JSONResponse(status_code=401, content={"detail": "invalid api key"})

        audit_event("api.request", actor)
        return await call_next(request)
