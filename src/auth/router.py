import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated, Union
from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

import database.queries as db
from auth.schemas import *
from config.config import JWT_SECRET_KEY, JWT_ALGORITHM
from custom_exceptions import *

auth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    user = await db.get_user_by_username(username)
    if user:
        return UserAllData.model_validate(user)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        raise NoUserFound
    
    if not verify_password(password, user.hashed_password):
        raise IncorrectPassword
    
    return user

@auth_router.post("/register", response_model=UserPublic)
async def register_user(user: UserNew):
    existing_user = await get_user(username=user.username)
    if existing_user:
        raise UserAlreadyExists

    hashed_password = get_password_hash(user.password)

    new_user = await db.add_user(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    return UserPublic.model_validate(new_user)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    if token is None:
        raise CredentialsError
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise EmptyPayload
        
    except InvalidTokenError:
        raise InvalidToken
    
    user = await get_user(username=username)
    if user is None:
        raise NoUserFound
    return user

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme)):
    try:
        return await get_current_user(token)
    except Exception as e:
        return None

@auth_router.get("/me/", response_model=Union[UserPublic, StandardResponse])
async def read_users_me(
    current_user: Optional[UserPublic] = Depends(get_current_user_optional),
):
    if current_user:
        return current_user
    return StandardResponse(result="No user logged in. Please register and authenticate")
