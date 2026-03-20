from typing import List, Optional  # 新增 Optional
from fastapi import APIRouter, Depends, HTTPException, Query  # 新增 Query
from ..schemas.user import UserCreate, UserRead
from ..service.user import UserService
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.database import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """创建用户"""
    return await UserService.create_user(session, user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """获取用户"""
    user = await UserService.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 核心修改：添加 zhanghao/xingming 可选搜索参数
@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    zhanghao: Optional[str] = Query(None),  # 新增：账号搜索（可选）
    xingming: Optional[str] = Query(None),  # 新增：姓名搜索（可选）
    session: AsyncSession = Depends(get_session)
):
    """获取用户列表（支持账号/姓名搜索）"""
    return await UserService.get_users(session, skip, limit, zhanghao, xingming)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate, session: AsyncSession = Depends(get_session)):
    """更新用户"""
    updated = await UserService.update_user(session, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """删除用户"""
    success = await UserService.delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}