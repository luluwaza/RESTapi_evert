import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("uvicorn.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        client_ip = request.client.host
        method = request.method
        path = request.url.path
        version = request.scope.get("http_version", "1.1")
        status_code = response.status_code

        # ✅ Pass the expected 5-tuple as args
        logger.info(
            '%s - "%s %s HTTP/%s" %s',
            client_ip,
            method,
            path,
            version,
            status_code,
        )

        # Optional: You can still print duration to a separate logger if you want

        return response
