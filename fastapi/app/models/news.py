from sqlmodel import SQLModel, Field, ForeignKey
from datetime import datetime
from typing import Optional


class News(SQLModel, table=True):
    __tablename__ = "news"
    __table_args__ = {"comment": "公告信息"}

    id: Optional[int] = Field(default=None, primary_key=True, description="主键")
    addtime: datetime = Field(default_factory=datetime.now, description="创建时间")
    title: str = Field(max_length=200, description="标题")  # 无 default → 非空
    introduction: Optional[str] = Field(default=None, description="简介")
    typename: Optional[str] = Field(max_length=200, default=None, description="分类名称")
    name: Optional[str] = Field(max_length=200, default=None, description="发布人")
    headportrait: Optional[str] = Field(default=None, description="头像")
    clicknum: Optional[int] = Field(default=0, description="点击次数")
    clicktime: Optional[datetime] = Field(default=None, description="最近点击时间")
    thumbsupnum: Optional[int] = Field(default=0, description="赞")
    crazilynum: Optional[int] = Field(default=0, description="踩")
    storeupnum: Optional[int] = Field(default=0, description="收藏数")
    picture: str = Field(description="图片")  # 无 default → 非空
    content: str = Field(description="内容")