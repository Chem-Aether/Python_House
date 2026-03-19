from fastapi import APIRouter, Depends, HTTPException
from ..core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..service.user import UserService
from ..service.admin import AdminService
from ..schemas.user import UserCreate
# Admin registration is disabled. AdminCreate import removed to prevent admin self-registration.
from pydantic import BaseModel
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

# 简单的内存 token 存储（演示）
TOKENS = {}


class LoginRequest(BaseModel):
    account: str
    password: str
    role: str = "user"  # user or admin


@router.post("/login")
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    """简单登录：根据 role 查用户或管理员，匹配密码（明文），返回 token"""
    if payload.role == 'admin':
        admin = await AdminService.get_by_username(session, payload.account)
        if not admin or admin.password != payload.password:
            raise HTTPException(status_code=401, detail='账号或密码错误')
        token = secrets.token_urlsafe(32)
        TOKENS[token] = {'role': 'admin', 'id': admin.id}
        return {'code': 200, 'data': {'token': token, 'role': 'admin'}}

    # 默认 user
    user = await UserService.get_by_zhanghao(session, payload.account)
    if not user or user.mima != payload.password:
        raise HTTPException(status_code=401, detail='账号或密码错误')
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {'role': 'user', 'id': user.id}
    return {'code': 200, 'data': {'token': token, 'role': 'user'}}


class RegisterRequest(BaseModel):
    account: str
    password: str
    xingming: str  # 姓名，数据库为 NOT NULL，需要前端提供


@router.post('/register')
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)):
    """简单注册：仅创建普通用户（明文密码，仅演示）。管理员不能通过此接口注册。"""
    # 强制创建用户账号；要求提供姓名（xingming）以匹配数据库约束
    existing = await UserService.get_by_zhanghao(session, payload.account)
    if existing:
        raise HTTPException(status_code=400, detail='用户已存在')
    user = await UserService.create_user(session, UserCreate(zhanghao=payload.account, mima=payload.password, xingming=payload.xingming))
    return {'code': 200, 'data': {'id': user.id, 'zhanghao': user.zhanghao}}


@router.get('/me')
async def me(token: str):
    info = TOKENS.get(token)
    if not info:
        raise HTTPException(status_code=401, detail='无效 token')
    return {'code': 200, 'data': info}
