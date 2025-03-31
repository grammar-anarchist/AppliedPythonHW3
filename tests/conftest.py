import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def access_token():
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