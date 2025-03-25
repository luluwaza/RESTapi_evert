from fastapi import APIRouter, Depends
from app.middleware.versioning import get_api_version

router = APIRouter()


@router.get("/hello")
def hello_world(version: str = Depends(get_api_version)):
    return {"version": version, "message": "hello world"}
