def register_user(client, email, name, password="SecurePassword123!"):
    res = client.post("/users", json={"email": email, "name": name, "password": password})
    return res.json()["id"]

def login_headers(client, email, password="SecurePassword123!"):
    res = client.post("/auth/token", data={"username": email, "password": password})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}

def test_note_lifecycle_and_authorization(client):
    """Test note creation, retrieval, privacy boundaries, and deletion."""
    alice_id = register_user(client, "alice@example.com", "Alice Smith")
    alice_headers = login_headers(client, "alice@example.com")
    
    register_user(client, "bob@example.com", "Bob Jones")
    bob_headers = login_headers(client, "bob@example.com")

    team_res = client.post("/teams", json={"name": "Security Team"}, headers=alice_headers)
    team_id = team_res.json()["id"]

    note_payload = {
        "text": "Confidential database credentials.",
        "visibility": "PRIVATE",
        "team_id": team_id,
    }
    create_res = client.post(f"/notes?owner_user_id={alice_id}", json=note_payload, headers=alice_headers)
    assert create_res.status_code in (200, 201)
    note_id = create_res.json()["id"]

    get_res = client.get(f"/notes/{note_id}", headers=alice_headers)
    assert get_res.status_code == 200
    assert get_res.json()["text"] == "Confidential database credentials."

    unauthorized_res = client.get(f"/notes/{note_id}", headers=bob_headers)
    assert unauthorized_res.status_code in (403, 404)

    delete_res = client.delete(f"/notes/{note_id}", headers=alice_headers)
    assert delete_res.status_code in (200, 204)

    verify_res = client.get(f"/notes/{note_id}", headers=alice_headers)
    assert verify_res.status_code == 404