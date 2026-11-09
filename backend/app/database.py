import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://reviews_user:change_this_password@db:5432/scientific_reviews"
)

engine = create_async_engine(
    DATABASE_URL,
    echo = True
)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
