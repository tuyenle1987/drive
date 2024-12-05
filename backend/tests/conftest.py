import pytest
from app import app
from flask import session

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"
    app.secret_key = "test_secret_key"
    
    with app.app_context():
        with app.test_client() as client:
            yield client

@pytest.fixture
def mock_session(client):
    with client.session_transaction() as sess:
        sess["credentials"] = '{"token": "fake_token", "refresh_token": "fake_refresh", "client_id": "test_client_id", "client_secret": "test_client_secret"}'
    yield sess
