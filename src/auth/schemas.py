from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = {'from_attributes': True}

class UserNew(UserBase):
    password: str

class UserPublic(UserBase):
    registered_at: Optional[datetime] = None

class UserAllData(UserPublic):
    id: int
    hashed_password: str

class StandardResponse(BaseModel):
    result: str
