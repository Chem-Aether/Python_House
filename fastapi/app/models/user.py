from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """用户数据模型，对应设计文档中 `users` 表的简化字段"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    addtime: datetime = Field(default_factory=datetime.utcnow)
    zhanghao: str = Field(index=True, nullable=False)
    mima: str = Field(nullable=False)
    xingming: Optional[str] = None
    touxiang: Optional[str] = None
    xingbie: Optional[str] = None
    nianling: Optional[int] = None
    shouji: Optional[str] = None