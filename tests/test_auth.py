import uuid

def test_user_registration_and_authentication(client):
    """Test user signup and OAuth2 token exchange."""
    unique_email = f"charlie_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "name": "Charlie Brown",
        "password": "Password123!",
    }
    res = client.post("/users", json=payload)
    assert res.status_code in (200, 201), f"Registration failed: {res.text}"
    data = res.json()
    assert data["email"] == unique_email
    assert "id" in data

    login_res = client.post("/auth/token", data={"username": unique_email, "password": "Password123!"})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    assert "access_token" in login_res.json()
    assert login_res.json()["token_type"] == "bearer"