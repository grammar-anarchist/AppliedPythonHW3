import os
import yaml
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL_SYNC = DB_URL.replace("postgresql+asyncpg", "postgresql+psycopg")

config_folder = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(config_folder, "settings.yaml"), "r") as file:
    settings = yaml.safe_load(file)

JWT_ALGORITHM = settings["jwt_algorithm"]
