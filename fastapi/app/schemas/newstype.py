from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List

# 基础模型
class NewsTypeBase(SQLModel):
    typename: str = Field(max_length=200, description="分类名称")

# 创建/更新模型
class NewsTypeCreate(NewsTypeBase):
    pass

class NewsTypeUpdate(NewsTypeBase):
    pass

# 响应模型
class NewsTypeRead(NewsTypeBase):
    id: int
    addtime: datetime

    # ✅ 修复：orm_mode → from_attributes（Pydantic V2 兼容）
    class Config:
        from_attributes = True

# 分页响应模型
class NewsTypePagination(SQLModel):
    items: List[NewsTypeRead]
    total: int
    page: int
    page_size: int