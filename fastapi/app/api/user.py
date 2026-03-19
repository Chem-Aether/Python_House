from typing import List

from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    """获取用户列表"""
    return await UserService.get_users(session, skip, limit)


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