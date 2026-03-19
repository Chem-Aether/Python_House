from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
