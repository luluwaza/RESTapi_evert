from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError

from app.core.security import require_role, get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["admin-users"])


def admin_required(current_user: User = Depends(require_role("admin"))):
    print(f"[admin_required] User: {current_user.username}, Role: {current_user.role}")
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


@router.get("/admin/users", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return db.query(User).all()


@router.get("/admin/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/admin/users", response_model=UserRead, status_code=201)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if user_in.role not in ("user", "admin"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Allowed values are: 'user', 'admin'.",
        )
    try:
        user = User(
            username=user_in.username,
            hashed_password=user_in.hashed_password,
            role=user_in.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        if "ix_users_username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_in.username}' already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error.",
        )


@router.delete("/admin/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return


@router.post("/refresh")
def refresh_token(request: Request, user: User = Depends(get_current_user)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split("Bearer ")[-1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if not exp:
            raise HTTPException(status_code=400, detail="Token missing expiration")

        now = datetime.now(timezone.utc)
        new_exp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload["exp"] = int(new_exp.timestamp())

        extended_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Replace token with updated token in response (assume same token handling client-side)
        return {"access_token": extended_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
