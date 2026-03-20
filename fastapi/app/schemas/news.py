from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List

# 基础模型
class NewsBase(SQLModel):
    title: str = Field(max_length=200, description="标题")
    introduction: Optional[str] = Field(default=None, description="简介")
    typename: Optional[str] = Field(max_length=200, default=None, description="分类名称")
    name: Optional[str] = Field(max_length=200, default=None, description="发布人")
    headportrait: Optional[str] = Field(default=None, description="头像")
    clicknum: Optional[int] = Field(default=0, description="点击次数")
    clicktime: Optional[datetime] = Field(default=None, description="最近点击时间")
    thumbsupnum: Optional[int] = Field(default=0, description="赞")
    crazilynum: Optional[int] = Field(default=0, description="踩")
    storeupnum: Optional[int] = Field(default=0, description="收藏数")
    picture: str = Field(description="图片")
    content: str = Field(description="内容")

# 创建模型
class NewsCreate(NewsBase):
    pass

# 更新模型
class NewsUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200, description="标题")
    introduction: Optional[str] = Field(default=None, description="简介")
    typename: Optional[str] = Field(default=None, max_length=200, description="分类名称")
    name: Optional[str] = Field(default=None, max_length=200, description="发布人")
    headportrait: Optional[str] = Field(default=None, description="头像")
    clicknum: Optional[int] = Field(default=None, description="点击次数")
    clicktime: Optional[datetime] = Field(default=None, description="最近点击时间")
    thumbsupnum: Optional[int] = Field(default=None, description="赞")
    crazilynum: Optional[int] = Field(default=None, description="踩")
    storeupnum: Optional[int] = Field(default=None, description="收藏数")
    picture: Optional[str] = Field(default=None, description="图片")
    content: Optional[str] = Field(default=None, description="内容")

# 响应模型
class NewsRead(NewsBase):
    id: int
    addtime: datetime

    # ✅ 修复：orm_mode → from_attributes
    class Config:
        from_attributes = True

# 分页响应模型
class NewsPagination(SQLModel):
    items: List[NewsRead]
    total: int
    page: int
    page_size: int