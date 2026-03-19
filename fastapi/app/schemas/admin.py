from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdminCreate(BaseModel):
    username: str
    password: str


class AdminRead(BaseModel):
    id: int
    username: str
    image: Optional[str] = None
    role: Optional[str] = None
    addtime: datetime

    class Config:
        from_attributes = True
