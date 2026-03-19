from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Admin(SQLModel, table=True):
    __tablename__ = 'admin'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)
    image: Optional[str] = None
    role: Optional[str] = '管理员'
    addtime: datetime = Field(default_factory=datetime.utcnow)
