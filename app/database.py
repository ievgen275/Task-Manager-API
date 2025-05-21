from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL_asyncpg)
new_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)