def test_team_lifecycle_and_members(client, register_user, login_headers):
    """Test team creation and member association."""
    alice_id, alice_email = register_user(email_prefix="alice", name="Alice Smith")
    alice_headers = login_headers(alice_email)
    
    bob_id, _ = register_user(email_prefix="bob", name="Bob Jones")

    team_res = client.post("/teams", json={"name": "Platform Engineering"}, headers=alice_headers)
    assert team_res.status_code in (200, 201), f"Team creation failed: {team_res.text}"
    team_id = team_res.json()["id"]
    assert team_res.json()["name"] == "Platform Engineering"

    add_member_res = client.post(
        f"/teams/{team_id}/members",
        json={"team_id": team_id, "user_id": bob_id},
        headers=alice_headers
    )
    assert add_member_res.status_code in (200, 201), f"Adding member failed: {add_member_res.text}"