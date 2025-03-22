import functools
from sqlalchemy import text

from database.session import get_session
from database.models import User, URL
from custom_exceptions import DBModificationFailure

def db_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async for db in get_session():
            return await func(db, *args, **kwargs)
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
    try:
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {e}")
        raise DBModificationFailure
