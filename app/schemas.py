from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmaBase(BaseModel):
    name: Optional[str] = Field(None, max_length=32)
    message: str = Field(..., max_length=280)
    type: Optional[str] = Field(None, max_length=16)

class EmaCreate(EmaBase):
    pass

class EmaRead(EmaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
