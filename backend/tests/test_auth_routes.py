import pytest
from unittest.mock import patch
from flask import session


@pytest.fixture
def client():
    from app import app
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_session(client):
    with client.session_transaction() as sess:
        sess["credentials"] = '{"token": "fake_token"}'
    yield sess


def test_login_redirect(client):
    response = client.get("/auth/login")
    assert response.status_code == 302
    assert "accounts.google.com" in response.location


@patch("services.auth_service.get_auth_url")
def test_login_custom_redirect(mock_get_auth_url, client):
    mock_url = "http://mock-auth-url.com"
    mock_get_auth_url.return_value = mock_url

    response = client.get("/auth/login")
    assert response.status_code == 302

def test_auth_status_not_authenticated(client):
    response = client.get("/auth/status")
    data = response.get_json()
    assert response.status_code == 200
    assert data["isAuthenticated"] is False


def test_auth_status_authenticated(client, mock_session):
    response = client.get("/auth/status")
    data = response.get_json()
    assert response.status_code == 200
    assert data["isAuthenticated"] is True


def test_logout(client, mock_session):
    response = client.post("/auth/logout")
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Logged out successfully"
    with client.session_transaction() as sess:
        assert "credentials" not in sess
