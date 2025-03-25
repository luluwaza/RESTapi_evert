from pydantic import BaseModel
from datetime import datetime


class RequestLogRead(BaseModel):
    id: int
    method: str
    path: str
    status_code: int
    client_ip: str
    duration: float
    timestamp: datetime

    class Config:
        from_attributes = True
