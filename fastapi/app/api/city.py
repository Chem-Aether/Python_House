from fastapi import APIRouter, Depends, HTTPException, Header
from ..core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..service.city import CityService
from ..schemas.city import CityCreate, CityRead

# 简单管理员校验：从 Authorization header 读取 Bearer token，并检查 token 在 auth 模块的 TOKENS 中且 role 为 'admin'
from ..api.auth import TOKENS


async def admin_required(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='未授权')
    token = authorization.split(' ', 1)[1]
    info = TOKENS.get(token)
    if not info or info.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='管理员权限不足')
    return info

router = APIRouter(prefix='/city', tags=['city'])


@router.get('/', response_model=list[CityRead])
async def list_cities(page: int = 1, page_size: int = 20, q: str | None = None, session: AsyncSession = Depends(get_session), _u=Depends(admin_required)):
    skip = (page - 1) * page_size
    items = await CityService.list_cities(session, skip=skip, limit=page_size, q=q)
    return items


@router.post('/', response_model=CityRead)
async def create_city(payload: CityCreate, session: AsyncSession = Depends(get_session), _u=Depends(admin_required)):
    city = await CityService.create_city(session, payload)
    return city


@router.get('/{city_id}', response_model=CityRead)
async def get_city(city_id: int, session: AsyncSession = Depends(get_session), _u=Depends(admin_required)):
    city = await CityService.get_city(session, city_id)
    if not city:
        raise HTTPException(status_code=404, detail='Not found')
    return city


@router.put('/{city_id}', response_model=CityRead)
async def update_city(city_id: int, payload: CityCreate, session: AsyncSession = Depends(get_session), _u=Depends(admin_required)):
    city = await CityService.update_city(session, city_id, payload)
    if not city:
        raise HTTPException(status_code=404, detail='Not found')
    return city


@router.delete('/{city_id}')
async def delete_city(city_id: int, session: AsyncSession = Depends(get_session), _u=Depends(admin_required)):
    ok = await CityService.delete_city(session, city_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Not found')
    return {'code': 200}
