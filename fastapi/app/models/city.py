from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class City(SQLModel, table=True):
    __tablename__ = 'city'

    id: Optional[int] = Field(default=None, primary_key=True)
    addtime: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    usetype: Optional[str] = Field(default=None)
    niandai: Optional[str] = Field(default=None)
    areanum: Optional[float] = Field(default=None)
    avgprice: Optional[float] = Field(default=None)
    zongjia: Optional[str] = Field(default=None)
    floorlevel: Optional[str] = Field(default=None)
    roomtype: Optional[str] = Field(default=None)
    laiyuan: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    clicktime: Optional[datetime] = Field(default=None)
    clicknum: Optional[int] = Field(default=0)
    discussnum: Optional[int] = Field(default=0)
    storeupnum: Optional[int] = Field(default=0)
