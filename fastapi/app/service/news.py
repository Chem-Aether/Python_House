from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from ..models.news import News
from ..schemas.news import NewsCreate, NewsUpdate
from datetime import datetime


class NewsService:
    @staticmethod
    async def get_news_list(
            session: AsyncSession,
            page: int = 1,
            page_size: int = 20,
            title: str = None,
            typename: str = None
    ):
        """获取新闻列表（分页+搜索）"""
        # 构建查询
        stmt = select(News)
        if title:
            stmt = stmt.where(News.title.like(f"%{title}%"))
        if typename:
            stmt = stmt.where(News.typename == typename)

        # 总数
        count_stmt = select(func.count(News.id))
        if title:
            count_stmt = count_stmt.where(News.title.like(f"%{title}%"))
        if typename:
            count_stmt = count_stmt.where(News.typename == typename)
        total = await session.scalar(count_stmt)

        # 列表
        stmt = stmt.offset((page - 1) * page_size).limit(page_size).order_by(News.addtime.desc())
        result = await session.exec(stmt)
        items = result.all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }

    @staticmethod
    async def get_news_by_id(session: AsyncSession, news_id: int):
        """根据ID获取新闻"""
        stmt = select(News).where(News.id == news_id)
        result = await session.exec(stmt)
        news = result.first()
        if not news:
            raise HTTPException(status_code=404, detail="新闻不存在")
        return news

    @staticmethod
    async def create_news(session: AsyncSession, news_data: NewsCreate):
        """创建新闻"""
        db_news = News(**news_data.dict())
        session.add(db_news)
        await session.commit()
        await session.refresh(db_news)
        return db_news

    @staticmethod
    async def update_news(session: AsyncSession, news_id: int, news_data: NewsUpdate):
        """更新新闻"""
        db_news = await NewsService.get_news_by_id(session, news_id)

        # 更新字段
        update_data = news_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_news, key, value)

        await session.commit()
        await session.refresh(db_news)
        return db_news

    @staticmethod
    async def delete_news(session: AsyncSession, news_id: int):
        """删除新闻"""
        db_news = await NewsService.get_news_by_id(session, news_id)
        await session.delete(db_news)
        await session.commit()
        return {"message": "新闻删除成功"}

    @staticmethod
    async def update_click_num(session: AsyncSession, news_id: int):
        """更新点击次数和最近点击时间"""
        db_news = await NewsService.get_news_by_id(session, news_id)
        db_news.clicknum = (db_news.clicknum or 0) + 1
        db_news.clicktime = datetime.now()
        await session.commit()
        await session.refresh(db_news)
        return db_news