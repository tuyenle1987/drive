from unittest.mock import patch
from services.auth_service import get_auth_url, handle_callback
from flask import session

@patch("services.auth_service.create_flow")
def test_get_auth_url(mock_create_flow):
    mock_flow = mock_create_flow.return_value
    mock_flow.authorization_url.return_value = ("http://mock-url", None)
    auth_url = get_auth_url()
    assert auth_url == "http://mock-url"

@patch("services.auth_service.create_flow")
def test_handle_callback(mock_create_flow, client):
    mock_flow = mock_create_flow.return_value
    mock_flow.fetch_token.return_value = None
    mock_flow.credentials.to_json.return_value = '{"token": "test"}'

    with client.application.test_request_context('/auth/callback'):
        handle_callback("http://callback-url")
        assert session["credentials"] == '{"token": "test"}'