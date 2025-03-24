import re
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from typing import Optional

import database.queries as db
from auth.router import get_current_user, get_current_user_optional
from auth.schemas import UserPublic, UserAllData
from tasks.tasks import delete_link_at_time
from links.schemas import *
from custom_exceptions import *

links_router = APIRouter(prefix="/links", tags=["links"])

reserved = ["shorten", "search"]

def forbidden_alias(alias: str) -> bool:
    return not bool(re.match(r"^[a-zA-Z0-9_-]+$", alias)) or \
        alias.isdigit() or (alias in reserved) or len(alias) == 0

async def unavailable_alias(alias: str) -> bool:
    url = await db.get_url_by_tiny_url(alias)
    return url is not None

@links_router.post("/shorten", response_model=ShortenResponse)
async def shorten_link(
    request: ShortenRequest, 
    current_user: Optional[UserAllData] = Depends(get_current_user_optional)
):
    if current_user:
        user_id = current_user.id
    else:
        user_id = None

    if request.alias:
        if await unavailable_alias(request.alias):
            raise UnavailableAlias
        
        if forbidden_alias(request.alias):
            raise ForbiddenAlias

    url = await db.add_url(user_id, request.alias, request.original_url, 
                           request.expires_at, request.redundant_period)

    if url.expires_at:
        delete_link_at_time.apply_async((url.id,), eta=url.expires_at)

    return ShortenResponse(short_code=url.tiny_url)

@links_router.get("/search", response_model=SearchResponse)
async def search_link(original_url: str):
    short_codes_lst = await db.get_tiny_urls_by_original_url(original_url)
    return SearchResponse(tiny_urls=short_codes_lst)

@links_router.delete("/{short_code}", response_model=DeleteResponse)
async def delete_link(
    short_code: str, 
    current_user: UserAllData = Depends(get_current_user)
):
    url = await db.get_url_by_tiny_url(short_code)
    if url is None:
        raise NoURLFound

    if url.user_id != current_user.id:
        raise ForbiddenAction
    
    original_url  = url.original_url
    
    await db.delete_url(url.id)
    return DeleteResponse(result=f'The short code {short_code} for URL {original_url} has been deleted.')

@links_router.put("/{short_code}", response_model=ChangeResponse)
async def change_link(
    short_code: str, 
    request: ChangeRequest,
    current_user: UserAllData = Depends(get_current_user)
):
    url = await db.get_url_by_tiny_url(short_code)
    if url is None:
        raise NoURLFound
    
    if url.user_id != current_user.id:
        raise ForbiddenAction
    
    await db.change_url(url.id, request.new_url)
    return ChangeResponse(result=f'The short code {short_code} now stands for {request.new_url}.')

@links_router.get("/{short_code}/stats", response_model=StatsResponse)
async def get_stats(short_code: str):
    url = await db.get_url_by_tiny_url(short_code)
    if url is None:
        raise NoURLFound
    
    return StatsResponse(original_url=url.original_url,
        created_at=url.created_at,
        clicks=url.usage_count,
        last_used_at=url.last_used_at
    )

@links_router.get("/{short_code}", response_class=RedirectResponse)
async def redirect(short_code: str):
    url = await db.get_url_by_tiny_url(short_code)
    if url is None:
        raise NoURLFound
    
    await db.record_usage(url.id)
    
    return RedirectResponse(url.original_url)
