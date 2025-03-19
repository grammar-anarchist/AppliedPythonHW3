from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config.config import DB_URL

engine = create_async_engine(DB_URL, pool_size=5, max_overflow=10 )
create_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_session() as session:
        yield session
