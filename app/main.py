from fastapi import FastAPI
from app.api.v1.endpoints import router as v1_router

app = FastAPI()

app.include_router(v1_router)