from datetime import datetime, timezone
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List

class ShortenRequest(BaseModel):
    original_url: str
    alias: Optional[str] = None
    expires_at: Optional[datetime] = None
    redundant_period: Optional[int] = None

    @field_validator("expires_at")
    def ensure_correct_expires_at_timezone(cls, value):
        if value and value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

class ShortenResponse(BaseModel):
    short_code: str

class SearchResponse(BaseModel):
    tiny_urls: List[str]

class DeleteResponse(BaseModel):
    result: str

class ChangeRequest(BaseModel):
    new_url: str

class ChangeResponse(BaseModel):
    result: str

class StatsResponse(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_used_at: Optional[datetime]
