"""
Shared pytest fixtures for the LicensingServer test suite.

Each test gets:
- A fresh in-memory SQLite database (full isolation, no shared state)
- PostgreSQL startup hooks mocked out (no live database required)
- Rate limiting disabled
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.dependencies import get_session
from app.utils.rsa_verification import RSAVerifier
import app.core.signing as signing
from app.core.rate_limiting import limiter


@pytest.fixture(scope="session", autouse=True)
def disable_rate_limiting():
    original = limiter.enabled
    limiter.enabled = False
    yield
    limiter.enabled = original


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def rsa_key_pair():
    return RSAVerifier.generate_key_pair()


@pytest.fixture
def client(db_session, rsa_key_pair):
    private_pem, _ = rsa_key_pair
    signing._private_key_pem = private_pem

    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with patch("app.main.wait_for_postgres_ready", new_callable=AsyncMock), \
         patch("app.main.init_postgres_schema", new_callable=AsyncMock), \
         patch("app.main.init_signing_key"):
        with TestClient(app) as test_client:
            yield test_client

    app.dependency_overrides.clear()
    signing._private_key_pem = None


@pytest.fixture
def auth_headers(client):
    client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "Secure1234!",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "Secure1234!",
    })
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    return {"Authorization": f"Bearer {resp.json()['session_token']}"}


@pytest.fixture
def license_key(client, auth_headers):
    customer = client.post(
        "/api/v1/customers/",
        json={"name": "Test Customer", "email": "customer@example.com"},
        headers=auth_headers,
    )
    assert customer.status_code == 201

    application = client.post(
        "/api/v1/applications/",
        json={"name": "Test App", "version": "1.0.0"},
        headers=auth_headers,
    )
    assert application.status_code == 201

    license_resp = client.post(
        "/api/v1/licenses/",
        json={
            "customer_id": customer.json()["id"],
            "application_id": application.json()["id"],
            "max_activations": 5,
        },
        headers=auth_headers,
    )
    assert license_resp.status_code == 201
    return license_resp.json()["license_key"]
