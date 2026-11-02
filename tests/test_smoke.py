
from fastapi.testclient import TestClient

from app.main import app


def test_full_application_smoke_flow(client):
    # 1. Register User A (Alice)
    alice_payload = {
        "email": "alice@example.com",
        "password": "SecurePassword123!",
        "name": "Alice Smith",
    }

    res = client.post("/users", json=alice_payload)
    assert res.status_code in (200, 201), res.text

    alice_user_id = res.json()["id"]

    # 2. Login User A
    login_payload = {
        "username": "alice@example.com",
        "password": "SecurePassword123!",
    }

    res = client.post("/auth/token", data=login_payload)
    assert res.status_code == 200, res.text

    alice_headers = {
        "Authorization": f"Bearer {res.json()['access_token']}"
    }

    # 3. Create a Team
    res = client.post(
        "/teams",
        json={"name": "Engineering"},
        headers=alice_headers,
    )

    assert res.status_code in (200, 201), res.text
    team_id = res.json()["id"]

    # 4. Create a Note
    note_payload = {
        "text": "Using FastAPI, SQLAlchemy 2.0, and SQLite.",
        "visibility": "PRIVATE",
        "team_id": team_id,
    }

    res = client.post(
        f"/notes?owner_user_id={alice_user_id}",
        json=note_payload,
        headers=alice_headers,
    )

    assert res.status_code in (200, 201), res.text
    note_id = res.json()["id"]

    # 5. Fetch Note as Alice
    res = client.get(
        f"/notes/{note_id}",
        headers=alice_headers,
    )

    assert res.status_code == 200
    assert res.json()["text"] == (
        "Using FastAPI, SQLAlchemy 2.0, and SQLite."
    )

    # 6. Register User B (Bob)
    bob_payload = {
        "email": "bob@example.com",
        "password": "SecurePassword123!",
        "name": "Bob Jones",
    }

    res = client.post("/users", json=bob_payload)
    assert res.status_code in (200, 201), res.text

    # 7. Login Bob
    res = client.post(
        "/auth/token",
        data={
            "username": "bob@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert res.status_code == 200, res.text

    bob_headers = {
        "Authorization": f"Bearer {res.json()['access_token']}"
    }

    # 8. Verify tenant isolation
    res = client.get(
        f"/notes/{note_id}",
        headers=bob_headers,
    )

    assert res.status_code in (403, 404), (
        f"Unauthorized access check failed: {res.status_code}"
    )


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
