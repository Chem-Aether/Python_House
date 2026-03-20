from typing import Optional
from datetime import datetime
from typing import Generic, TypeVar, List
from pydantic import BaseModel

# 通用分页模型
T = TypeVar('T')
class PageResponse(BaseModel, Generic[T]):
    items: List[T]  # 当前页数据列表
    total: int      # 总条数
    page: int       # 当前页码
    page_size: int  # 每页条数

class CityCreate(BaseModel):
    title: Optional[str] = None
    picture: Optional[str] = None
    usetype: Optional[str] = None
    niandai: Optional[str] = None
    areanum: Optional[float] = None
    avgprice: Optional[float] = None
    zongjia: Optional[str] = None
    floorlevel: Optional[str] = None
    roomtype: Optional[str] = None
    laiyuan: Optional[str] = None
    address: Optional[str] = None


class CityRead(BaseModel):
    id: int
    addtime: datetime
    title: Optional[str] = None
    picture: Optional[str] = None
    usetype: Optional[str] = None
    niandai: Optional[str] = None
    areanum: Optional[float] = None
    avgprice: Optional[float] = None
    zongjia: Optional[str] = None
    floorlevel: Optional[str] = None
    roomtype: Optional[str] = None
    laiyuan: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True
