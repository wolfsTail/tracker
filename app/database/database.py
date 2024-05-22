from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings import settings


DATABASE_URL = settings.ASYNC_DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
