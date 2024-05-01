from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import settings


DATABASE_URL = f"sqlite+aiosqlite:///{settings.DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
