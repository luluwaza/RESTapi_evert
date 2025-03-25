import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.db.session import SessionLocal
from app.models.request_log import RequestLog


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        db = SessionLocal()
        try:
            log = RequestLog(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                client_ip=request.client.host,
                duration=duration,
            )
            db.add(log)
            db.commit()
        finally:
            db.close()

        return response
