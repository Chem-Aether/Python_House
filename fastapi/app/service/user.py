from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ..models.user import User
from ..schemas.user import UserCreate
from typing import List, Optional


class UserService:
    """用户服务：实现基础的 CRUD 操作"""

    @staticmethod
    async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
        db_user = User(**user_data.dict())
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.exec(select(User).where(User.id == user_id))
        return result.first()

    @staticmethod
    async def get_by_zhanghao(session: AsyncSession, zhanghao: str) -> Optional[User]:
        """根据账号查找用户"""
        result = await session.exec(select(User).where(User.zhanghao == zhanghao))
        return result.first()

    @staticmethod
    async def get_users(session: AsyncSession, skip: int = 0, limit: int = 100, zhanghao: str = None,
                        xingming: str = None):
        """获取用户列表（支持搜索）"""
        query = select(User)  # 假设你的 User 模型是 sqlmodel 定义的

        # 新增：添加搜索条件
        if zhanghao:
            query = query.where(User.zhanghao.like(f"%{zhanghao}%"))
        if xingming:
            query = query.where(User.xingming.like(f"%{xingming}%"))

        # 分页
        query = query.offset(skip).limit(limit)

        result = await session.exec(query)
        return result.all()

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, user_data: UserCreate) -> Optional[User]:
        user = await UserService.get_user(session, user_id)
        if user:
            # 简单字段更新
            user.zhanghao = user_data.zhanghao
            user.mima = user_data.mima
            user.xingming = user_data.xingming
            user.touxiang = user_data.touxiang
            user.xingbie = user_data.xingbie
            user.nianling = user_data.nianling
            user.shouji = user_data.shouji
            user.addtime = datetime.utcnow()
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> bool:
        user = await UserService.get_user(session, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False