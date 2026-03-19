from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    zhanghao: str
    mima: str  # 明文密码，生产中应使用哈希
    xingming: Optional[str] = None
    touxiang: Optional[str] = None
    xingbie: Optional[str] = None
    nianling: Optional[int] = None
    shouji: Optional[str] = None


class UserRead(BaseModel):
    id: int
    addtime: datetime
    zhanghao: str
    xingming: Optional[str] = None
    touxiang: Optional[str] = None
    xingbie: Optional[str] = None
    nianling: Optional[int] = None
    shouji: Optional[str] = None

    class Config:
        from_attributes = True
