from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ..models.admin import Admin
from ..schemas.admin import AdminCreate
from typing import Optional


class AdminService:
    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> Optional[Admin]:
        result = await session.exec(select(Admin).where(Admin.username == username))
        return result.first()

    @staticmethod
    async def create_admin(session: AsyncSession, admin_data: AdminCreate) -> Admin:
        admin = Admin(**admin_data.dict())
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        return admin
