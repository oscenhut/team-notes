def test_health_check(client):
    """Test health check endpoint status."""
    response = client.get("/health")
    assert response.status_code == 200