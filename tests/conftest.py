import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.database import Base
from src.core.database import transactional
from src.core.config import settings

# Override the config to use the test database
TEST_URL = settings.TEST_URL


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(TEST_URL)
    session = async_sessionmaker(async_engine, expire_on_commit=False)

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        transactional.session = s
        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()
