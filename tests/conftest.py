import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def kill_tasks(event_loop):
    yield
    for task in asyncio.all_tasks(loop=event_loop):
        if not task.done() and "asyncpg" in repr(task):
            task.cancel()

@pytest.fixture(scope="function")
def access_token():
    with TestClient(app) as client:
        user_data = {
            "username": "common_user",
            "email": "valid@email.com",
            "password": "password"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code in (200, 400)

        access_token = client.post("/auth/token", data={
                "username": "common_user",
                "password": "password",
                "grant_type": "password",
                "scope": "",
                "client_id": "",
                "client_secret": ""
            }, 
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        ).json()["access_token"]
        
    return access_token
