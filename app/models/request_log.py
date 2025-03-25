from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.db.session import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    client_ip = Column(String)
    duration = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
