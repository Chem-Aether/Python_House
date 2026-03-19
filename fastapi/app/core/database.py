from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# 数据库连接URL
DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/django3ahrxq75?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 创建异步会话本地类
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_session():
    """获取数据库会话的依赖项"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()