from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class NewsType(SQLModel, table=True):
    __tablename__ = "newstype"
    __table_args__ = {"comment": "公告信息分类"}

    id: Optional[int] = Field(default=None, primary_key=True, description="主键")
    addtime: datetime = Field(default_factory=datetime.now, description="创建时间")
    typename: str = Field(max_length=200, description="分类名称")