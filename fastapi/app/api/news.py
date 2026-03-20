from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.news import NewsCreate, NewsRead, NewsUpdate, NewsPagination
from ..service.news import NewsService
from ..core.database import get_session

router = APIRouter(prefix="/news", tags=["新闻管理"])

# 获取新闻列表
@router.get("/", response_model=NewsPagination)
async def get_news_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    title: str = Query(None, description="标题模糊搜索"),
    typename: str = Query(None, description="分类名称筛选"),
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.get_news_list(session, page, page_size, title, typename)

# 获取单个新闻
@router.get("/{news_id}", response_model=NewsRead)
async def get_news(
    news_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.get_news_by_id(session, news_id)

# 创建新闻
@router.post("/", response_model=NewsRead)
async def create_news(
    news_data: NewsCreate,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.create_news(session, news_data)

# 更新新闻
@router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.update_news(session, news_id, news_data)

# 删除新闻
@router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.delete_news(session, news_id)

# 更新点击次数
@router.patch("/{news_id}/click")
async def update_news_click(
    news_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.update_click_num(session, news_id)