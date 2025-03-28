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
from app.models.user import User
from passlib.context import CryptContext
from fastapi import HTTPException
from app.api.v1.admin_users import router as admin_users_router

router = APIRouter()
router.include_router(admin_users_router)


@router.get("/logs", response_model=list[RequestLogRead])
def get_logs(
    db: Session = Depends(get_db),
    version: str = Depends(get_api_version),
    user=Depends(require_role("admin")),
    limit: int = 100,
):
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(limit).all()
    return logs


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(
    version: str = Depends(get_api_version),
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
