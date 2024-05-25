import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings as app_settings
from app.models.base import Base


@pytest.fixture
def settings():
    return app_settings

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/local_db_test"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionFactory = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_models():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all())
        await connection.run_sync(Base.metadata.create_all())
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all())

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    yield AsyncSessionFactory()
    await AsyncSessionFactory().close_all()
