from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession

def utcnow():
    return datetime.now(timezone.utc)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), default=utcnow)

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, default=None)
    original_url = Column(String, nullable=False)
    tiny_url = Column(String, unique=True, nullable=False,
        server_default=text("currval('urls_id_seq')::text"))
    created_at = Column(TIMESTAMP(timezone=True), default=utcnow)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(TIMESTAMP(timezone=True), nullable=True, default=None)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True, default=None)
    redundant_period = Column(Integer, nullable=False, default=14)

    user = relationship("User")
