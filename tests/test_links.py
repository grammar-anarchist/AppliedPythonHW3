import pytest
import time
from datetime import datetime, timedelta, timezone


def test_shorten_basic(client):
    data = {
        "original_url": "https://google.com"
    }
    response = client.post("/links/shorten", json=data)
    assert response.status_code == 200
    response = response.json()
    assert response["short_code"].isdigit()


def test_celery_worker(client):
    data = {
        "original_url": "https://yandex.ru",
        "expires_at": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    }
    response = client.post("/links/shorten", json=data)
    response = client.get("/links/search", params={"original_url": "https://yandex.ru"})
    assert len(response.json()["tiny_urls"]) == 1

    time.sleep(10)

    response = client.get("/links/search", params={"original_url": "https://yandex.ru"})
    assert len(response.json()["tiny_urls"]) == 0

def test_shorten_with_alias(client):
    data = {
        "original_url": "https://google.com",
        "alias": "google"
    }
    response = client.post("/links/shorten", json=data)
    assert response.status_code == 200
    response = response.json()
    assert response["short_code"] == "google"

    # alias already taken
    response = client.post("/links/shorten", json=data)
    assert response.status_code == 400

def test_shorten_forbidden_alias(client):
    data = {
        "original_url": "https://google.com",
        "alias": "1234" 
    }
    response = client.post("/links/shorten", json=data)
    assert response.status_code == 400
    
def test_search(client):
    client.post("/links/shorten", json={"original_url": "https://github.com"})
    client.post("/links/shorten", json={"original_url": "https://github.com"})
    client.post("/links/shorten", json={"original_url": "https://github.com"})

    response = client.get("/links/search", params={"original_url": "https://github.com"})
    assert response.status_code == 200
    response = response.json()
    assert len(response["tiny_urls"]) == 3

def test_delete(client, access_token):
    client.post("/links/shorten",
                 json={"original_url": "https://example.com", "alias": "deletion"}, 
                headers={"Authorization": f"Bearer {access_token}"}
    )

    response = client.get("/links/search", params={"original_url": "https://example.com"})
    assert response.json()["tiny_urls"] == ["deletion"]

    response = client.delete("/links/deletion", headers={"Authorization": f"Bearer {access_token}"})

    response = client.get("/links/search", params={"original_url": "https://example.com"})
    assert len(response.json()["tiny_urls"]) == 0

def test_delete_nonexistent(client, access_token):
    response = client.delete("/links/nonexistent", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400

def test_delete_unauthenticated(client):
    client.post("/links/shorten", json={"original_url": "https://unauth.com", "alias": "unauth_deletion"})

    response = client.delete("/links/unauth_deletion")
    assert response.status_code == 401

def test_change(client, access_token):
    client.post("/links/shorten", 
        json={"original_url": "https://change.com", "alias": "change"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    response = client.get("/links/search", params={"original_url": "https://change.com"})
    assert response.json()["tiny_urls"] == ["change"]

    client.put("/links/change", 
        json={"new_url": "https://changed.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    response = client.get("/links/search", params={"original_url": "https://change.com"})
    assert len(response.json()["tiny_urls"]) == 0

    response = client.get("/links/search", params={"original_url": "https://changed.com"})
    assert response.json()["tiny_urls"] == ["change"]

def test_change_nonexistent(client, access_token):
    response = client.put("/links/nonexistent", 
        json={"new_url": "https://changed.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400

def test_change_unauthenticated(client):
    client.post("/links/shorten", json={"original_url": "https://unauth.com", "alias": "unauth_change"})
    response = client.put("/links/unauth_change", json={"new_url": "https://changed.com"})
    assert response.status_code == 401

def test_redirect_nonexistent(client):
    response = client.get("/links/nonexistent")
    assert response.status_code == 400

def test_redirect(client):
    client.post("/links/shorten", json={"original_url": "https://redirect.com", "alias": "redirect"})

    response = client.get("/links/redirect")
    assert response.status_code == 307
    assert response.headers["Location"] == "https://redirect.com"

def test_stats(client):
    client.post("/links/shorten", json={"original_url": "https://stats.com", "alias": "stats"})

    for i in range(5):
        client.get("/links/stats")
    
    response = client.get("/links/stats/stats")
    response = response.json()
    assert response["clicks"] == 5
    assert response["original_url"] == "https://stats.com"
    assert response["last_used_at"] is not None
    assert datetime.fromisoformat(response["last_used_at"]) > datetime.now(timezone.utc) - timedelta(minutes=1)

def test_stats_nonexistent(client):
    response = client.get("/links/stats/nonexistent")
    assert response.status_code == 404
