from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.newstype import NewsTypeCreate, NewsTypeRead, NewsTypeUpdate, NewsTypePagination
from ..service.newstype import NewsTypeService
from ..core.database import get_session

router = APIRouter(prefix="/news/types", tags=["新闻分类管理"])

# 获取分类列表
@router.get("/", response_model=NewsTypePagination)
async def get_news_types(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    return await NewsTypeService.get_all_types(session, page, page_size)

# 获取单个分类
@router.get("/{type_id}", response_model=NewsTypeRead)
async def get_news_type(
    type_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await NewsTypeService.get_type_by_id(session, type_id)

# 创建分类
@router.post("/", response_model=NewsTypeRead)
async def create_news_type(
    type_data: NewsTypeCreate,
    session: AsyncSession = Depends(get_session)
):
    return await NewsTypeService.create_type(session, type_data)

# 更新分类
@router.put("/{type_id}", response_model=NewsTypeRead)
async def update_news_type(
    type_id: int,
    type_data: NewsTypeUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await NewsTypeService.update_type(session, type_id, type_data)

# 删除分类
@router.delete("/{type_id}")
async def delete_news_type(
    type_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await NewsTypeService.delete_type(session, type_id)