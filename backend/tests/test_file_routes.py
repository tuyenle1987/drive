from unittest.mock import patch, MagicMock
from io import BytesIO
from flask import Response
import json

MOCK_CREDENTIALS = {
    "token": "fake_token",
    "refresh_token": "fake_refresh_token",
    "client_secret": "fake_client_secret",
    "client_id": "fake_client_id",
}

@patch("services.drive_service.get_drive_service")
def test_list_files(mock_get_drive_service, client):
    """Test for listing files."""
    # Mock the Drive service
    mock_service = MagicMock()
    mock_files = {"files": [{"id": "1", "name": "test_file.txt"}]}
    mock_service.files().list().execute.return_value = mock_files
    mock_get_drive_service.return_value = mock_service

    # Mock credentials in the session
    with client.session_transaction() as sess:
        sess["credentials"] = json.dumps(MOCK_CREDENTIALS)

    response = client.get("/files")
    data = response.get_json()

    assert response.status_code == 200
    assert data["files"] == [{"id": "1", "name": "test_file.txt"}]

@patch("services.drive_service.get_drive_service")
def test_upload_file(mock_get_drive_service, client):
    """Test for uploading a file."""
    mock_service = MagicMock()
    mock_service.files().create().execute.return_value = {"id": "1"}
    mock_get_drive_service.return_value = mock_service

    with client.session_transaction() as sess:
        sess["credentials"] = json.dumps(MOCK_CREDENTIALS)

    data = {
        "file": (BytesIO(b"file content"), "test_file.txt"),
    }
    response = client.post("/files/upload", data=data, content_type="multipart/form-data")
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data["message"] == "File uploaded successfully"

@patch("services.drive_service.get_drive_service")
def test_delete_file(mock_get_drive_service, client):
    """Test for deleting a file."""
    mock_service = MagicMock()
    mock_service.files().delete().execute.return_value = {}
    mock_get_drive_service.return_value = mock_service

    with client.session_transaction() as sess:
        sess["credentials"] = json.dumps(MOCK_CREDENTIALS)

    response = client.delete("/files/delete/test_id")
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data["message"] == "File deleted successfully"
