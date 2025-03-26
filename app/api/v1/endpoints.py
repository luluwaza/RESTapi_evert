from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_role
from app.middleware.versioning import get_api_version
from app.models.request_log import RequestLog
from app.schemas.request_log import RequestLogRead
from app.db.dependencies import get_db

router = APIRouter()


@router.get("/hello")
def hello_world(version: str = Depends(get_api_version)):
    return {"version": version, "message": "hello world"}


@router.get("/logs", response_model=list[RequestLogRead])
def get_logs(
    db: Session = Depends(get_db),
    version: str = Depends(get_api_version),
    user=Depends(require_role("admin")),
    limit: int = 100,
):
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(limit).all()
    return logs
