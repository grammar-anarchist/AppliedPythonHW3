import pytest
from httpx import Client, AsyncClient
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

def test_me_unregistered(client):
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json() == {"result": "No user logged in. Please register and authenticate"}

def test_registration(client):
    data = {
        "username": "test",
        "email": "valid@email.com",
        "password": "password"
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 200
    response = response.json()
    assert response["username"] == "test"
    assert response["email"] == "valid@email.com"
    assert response["registered_at"] is not None
    assert datetime.fromisoformat(response["registered_at"]) > datetime.now(timezone.utc) - timedelta(minutes=1)

    response = client.post("/auth/register", json=data)
    assert response.status_code == 400

@pytest.mark.asyncio(loop_scope="function")
async def test_login_unregistered(async_client):
    data = {
        "username": "nonexistent",
        "password": "password",
        "grant_type": "password",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await async_client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 401

'''
def test_login():
    with TestClient(app) as client:
        data = {
            "username": "logger",
            "password": "password",
            "grant_type": "password",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = client.post("/auth/register", json={
            "username": "logger",
            "email": "valid@email.com",
            "password": "password"
        })

        response = client.post("/auth/token", data=data, headers=headers)
        assert response.status_code == 200
        response = response.json()
        assert "access_token" in response
        assert "token_type" in response

        # Wrong password
        data['password'] = 'wrong_password'
        response = client.post("/auth/token", data=data, headers=headers)
        assert response.status_code == 401
'''
'''
def test_me_registered(access_token):
    with TestClient(app) as client:
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        response = response.json()
        assert response["username"] == "common_user"
        assert response["email"] == "valid@email.com"
        assert response["registered_at"] is not None
'''
