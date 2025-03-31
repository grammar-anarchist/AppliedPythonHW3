import functools
from sqlalchemy import text
from datetime import datetime, timezone
from typing import Optional

from database.session import create_session
from database.models import User, URL
from links.schemas import *
from custom_exceptions import DBManipulationFailure

def db_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        sessionmaker = kwargs.pop("sessionmaker", create_session)
        async with sessionmaker() as db:
            try:
                return await func(db, *args, **kwargs)
            except Exception as e:
                await db.rollback()
                print(f"Error occurred: {e}")
                raise DBManipulationFailure

    return wrapper

@db_session
async def fetch_users(db):
    result = await db.execute("SELECT * FROM users;")
    return result.fetchall()

@db_session
async def get_user_by_username(db, username: str):
    query = text("SELECT * FROM users WHERE username = :username;")
    result = await db.execute(query, {"username": username})
    return result.fetchone()

@db_session
async def add_user(db, username: str, email: str, hashed_password: str):
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@db_session
async def tiny_url_exists(db, tiny_url: str) -> bool:
    query = text("SELECT EXISTS(SELECT 1 FROM urls WHERE tiny_url = :tiny_url);")
    result = await db.execute(query, {"tiny_url": tiny_url})
    return result.scalar_one()

@db_session
async def get_url_by_tiny_url(db, tiny_url: str):
    query = text("SELECT * FROM urls WHERE tiny_url = :tiny_url;")
    result = await db.execute(query, {"tiny_url": tiny_url})
    return result.fetchone()

@db_session
async def get_tiny_urls_by_original_url(db, original_url: str):
    query = text("SELECT tiny_url FROM urls WHERE original_url = :original_url;")
    result = await db.execute(query, {"original_url": original_url})
    return result.scalars().all()

@db_session
async def add_url(db, user_id: Optional[int], tiny_url: Optional[str], original_url: str, 
                expires_at: Optional[datetime], redundant_period: Optional[int]):
    url = URL(user_id=user_id, tiny_url=tiny_url, original_url=original_url, 
                expires_at=expires_at, redundant_period=redundant_period)
    db.add(url)
    await db.commit()
    await db.refresh(url)

    return url

@db_session
async def delete_url(db, id: int):
    query = text("DELETE FROM urls WHERE id = :id;")
    await db.execute(query, {"id": id})
    await db.commit()

@db_session
async def change_url(db, id: int, new_url: str):
    query = text("UPDATE urls SET original_url = :new_url WHERE id = :id;")
    await db.execute(query, {"id": id, "new_url": new_url})
    await db.commit()

@db_session
async def record_usage(db, id: int):
    last_used_at = datetime.now(timezone.utc)
    query = text("""
        UPDATE urls 
        SET usage_count = usage_count + 1, last_used_at = :last_used_at 
        WHERE id = :id;
    """)
    
    await db.execute(query, {"id": id, "last_used_at": last_used_at})
    await db.commit()

@db_session
async def delete_unpopular_links(db):
    query = text("""
        DELETE FROM urls
        WHERE (
            CASE 
                WHEN last_used_at IS NOT NULL THEN last_used_at
                ELSE created_at
            END
        ) < (CURRENT_TIMESTAMP - INTERVAL '1 day' * redundant_period);
    """)
    await db.execute(query)
    await db.commit()
