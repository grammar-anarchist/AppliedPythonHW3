import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from main import app

client = TestClient(app)

def test_me_unregistered():
    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json() == {"result": "No user logged in. Please register and authenticate"}

def test_registration():
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
    assert response["registered_at"] > datetime.now(timezone.utc) - timedelta(minutes=1)

    try:
        client.post("/auth/register", json=data)
        assert False
    except Exception as e:
        assert e.status_code == 400

def test_login():
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

    # Unregistered user
    try:
        client.post("/auth/token", data=data, headers=headers)
        assert False
    except Exception as e:
        assert e.status_code == 401

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
    try:
        client.post("/auth/token", data=data, headers=headers)
        assert False
    except Exception as e:
        assert e.status_code == 401

def test_me_registered(access_token):
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    response = response.json()
    assert response["username"] == "common_user"
    assert response["email"] == "valid@email.com"
    assert response["registered_at"] is not None
