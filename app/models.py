from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Ema(Base):
    __tablename__ = "emas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=True)
    message = Column(String(280), nullable=False)
    type = Column(String(16), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
