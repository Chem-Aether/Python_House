from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from ..models.city import City
from ..schemas.city import CityCreate
from typing import List, Optional


class CityService:
    @staticmethod
    async def create_city(session: AsyncSession, data: CityCreate) -> City:
        city = City(**data.dict())
        session.add(city)
        await session.commit()
        await session.refresh(city)
        return city

    @staticmethod
    async def get_city(session: AsyncSession, city_id: int) -> Optional[City]:
        result = await session.exec(select(City).where(City.id == city_id))
        return result.first()

    @staticmethod
    async def list_cities(session: AsyncSession, skip: int = 0, limit: int = 20, q: Optional[str] = None) -> List[City]:
        stmt = select(City)
        if q:
            stmt = stmt.where(City.title.contains(q))
        stmt = stmt.offset(skip).limit(limit)
        result = await session.exec(stmt)
        return result.all()

    @staticmethod
    async def count_cities(session: AsyncSession, q: str | None = None):
        query = select(func.count(City.id))  # 统计主键数量
        # 模糊搜索条件（同步修复 None 处理）
        if q:
            query = query.where(
                City.id.contains(q) |
                (City.address.is_not(None) & City.address.contains(q))
            )
        result = await session.exec(query)
        # 修复：新版本用 .one() 替代 .scalar()
        return result.one()  # 关键修复点

    @staticmethod
    async def update_city(session: AsyncSession, city_id: int, data: CityCreate) -> Optional[City]:
        city = await CityService.get_city(session, city_id)
        if not city:
            return None
        for k, v in data.dict().items():
            setattr(city, k, v)
        session.add(city)
        await session.commit()
        await session.refresh(city)
        return city

    @staticmethod
    async def delete_city(session: AsyncSession, city_id: int) -> bool:
        city = await CityService.get_city(session, city_id)
        if not city:
            return False
        await session.delete(city)
        await session.commit()
        return True
