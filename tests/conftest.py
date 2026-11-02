import os
import uuid

# 1. Force environment variable before any app modules load
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from app.main import app as fastapi_app
from app.database import Base, engine, get_db

# CRITICAL: Import all models explicitly so Base.metadata knows about them
import app.models.user
import app.models.team
import app.models.note
import app.models.user_team

print("Registered tables:", list(Base.metadata.tables.keys()))

@pytest.fixture(scope="session", autouse=True)
def setup_database_session():
    db_engine = engine

    Base.metadata.create_all(bind=db_engine)

    from app.database import get_engine

    print("TEST ENGINE ID:", id(get_engine()))
    

    print("Engine URL:", db_engine.url)
    print("Engine pool:", type(db_engine.pool).__name__)

    with db_engine.connect() as connection:
        from sqlalchemy import inspect
        inspector = inspect(connection)
        print("Actual DB tables:", inspector.get_table_names())

    yield

    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture(autouse=True)
def clean_tables():
    """Optionally clear table data between tests without dropping table schemas."""
    yield
    # If you want to truncate tables between tests instead of dropping schemas:
    with engine.connect() as connection:
        transaction = connection.begin()
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture
def register_user(client):
    """Fixture to register a user with a unique email and return (user_id, email)."""
    def _register(email_prefix="user", name="Test User", password="SecurePassword123!"):
        unique_email = f"{email_prefix}_{uuid.uuid4().hex[:8]}@example.com"
        payload = {"email": unique_email, "name": name, "password": password}
        res = client.post("/users", json=payload)
        assert res.status_code in (200, 201), f"Registration failed: {res.text}"
        data = res.json()
        return data["id"], unique_email
    return _register


@pytest.fixture
def login_headers(client):
    """Fixture to login and return Authorization bearer headers."""
    def _login(email, password="SecurePassword123!"):
        res = client.post("/auth/token", data={"username": email, "password": password})
        assert res.status_code == 200, f"Login failed for {email}: {res.text}"
        return {"Authorization": f"Bearer {res.json()['access_token']}"}
    return _login