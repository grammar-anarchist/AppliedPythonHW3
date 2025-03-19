import psycopg2
from config.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# python src/create_db.py
# Intended to run only once

def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cursor.fetchone()

    if not exists:
        print(f"Creating database: {DB_NAME}")
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
    else:
        print(f"Database {DB_NAME} already exists.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
