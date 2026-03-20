from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from ..models.newstype import NewsType
from ..schemas.newstype import NewsTypeCreate, NewsTypeUpdate


class NewsTypeService:
    @staticmethod
    async def get_all_types(session: AsyncSession, page: int = 1, page_size: int = 20):
        """获取所有分类（分页）"""
        # 总数
        count_stmt = select(func.count(NewsType.id))
        total = await session.scalar(count_stmt)

        # 列表
        stmt = select(NewsType).offset((page - 1) * page_size).limit(page_size)
        result = await session.exec(stmt)
        items = result.all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }

    @staticmethod
    async def get_type_by_id(session: AsyncSession, type_id: int):
        """根据ID获取分类"""
        stmt = select(NewsType).where(NewsType.id == type_id)
        result = await session.exec(stmt)
        news_type = result.first()
        if not news_type:
            raise HTTPException(status_code=404, detail="分类不存在")
        return news_type

    @staticmethod
    async def create_type(session: AsyncSession, type_data: NewsTypeCreate):
        """创建分类"""
        # 检查分类名称是否重复
        stmt = select(NewsType).where(NewsType.typename == type_data.typename)
        result = await session.exec(stmt)
        if result.first():
            raise HTTPException(status_code=400, detail="分类名称已存在")

        db_type = NewsType(**type_data.dict())
        session.add(db_type)
        await session.commit()
        await session.refresh(db_type)
        return db_type

    @staticmethod
    async def update_type(session: AsyncSession, type_id: int, type_data: NewsTypeUpdate):
        """更新分类"""
        db_type = await NewsTypeService.get_type_by_id(session, type_id)

        # 检查分类名称是否重复（排除自身）
        if type_data.typename != db_type.typename:
            stmt = select(NewsType).where(NewsType.typename == type_data.typename)
            result = await session.exec(stmt)
            if result.first():
                raise HTTPException(status_code=400, detail="分类名称已存在")

        # 更新字段
        update_data = type_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_type, key, value)

        await session.commit()
        await session.refresh(db_type)
        return db_type

    @staticmethod
    async def delete_type(session: AsyncSession, type_id: int):
        """删除分类"""
        db_type = await NewsTypeService.get_type_by_id(session, type_id)
        await session.delete(db_type)
        await session.commit()
        return {"message": "分类删除成功"}