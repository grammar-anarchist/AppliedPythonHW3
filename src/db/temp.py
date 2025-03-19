from db.session import get_db

async def fetch_users():
    async for db in get_db():  # Manually call get_db()
        result = await db.execute("SELECT * FROM users;")
        return result.fetchall()  # No need to close db, get_db() handles it
