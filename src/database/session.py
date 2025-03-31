from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import DB_URL

def create_sessionmaker_instance():
    engine = create_async_engine(DB_URL, pool_size=5, max_overflow=10 )
    create_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    return engine, create_session

engine, create_session = create_sessionmaker_instance()
