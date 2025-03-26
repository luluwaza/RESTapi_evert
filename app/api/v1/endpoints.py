from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_role
from app.middleware.versioning import get_api_version
from app.models.request_log import RequestLog
from app.schemas.request_log import RequestLogRead
from app.db.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import fake_users_db


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


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # No password check in fake DB — add later if needed
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
