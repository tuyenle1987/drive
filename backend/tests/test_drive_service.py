from unittest.mock import patch, MagicMock
from services.drive_service import list_files, upload_file, delete_file, download_file
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO

@patch("services.drive_service.get_drive_service")
def test_list_files(mock_get_drive_service):
    mock_service = mock_get_drive_service.return_value
    mock_service.files().list().execute.return_value = {"files": [{"id": "1", "name": "test_file.txt"}]}
    files = list_files()
    assert files == [{"id": "1", "name": "test_file.txt"}]

@patch("services.drive_service.get_drive_service")
def test_upload_file(mock_get_drive_service):
    mock_service = mock_get_drive_service.return_value
    mock_service.files().create().execute.return_value = {"id": "file_id"}
    
    class MockFile:
        filename = "test_file.txt"

        def save(self, destination_path):
            with open(destination_path, "w") as f:
                f.write("mock content")

    mock_file = MockFile()

    file_id = upload_file(mock_file)

    assert file_id == "file_id"


@patch("services.drive_service.get_drive_service")
def test_delete_file(mock_get_drive_service):
    mock_service = mock_get_drive_service.return_value
    delete_file("file_id")
    mock_service.files().delete.assert_called_with(fileId="file_id")

@patch("services.drive_service.get_drive_service")
@patch("services.drive_service.MediaIoBaseDownload")
def test_download_file(mock_downloader, mock_get_drive_service):
    mock_service = mock_get_drive_service.return_value
    mock_service.files().get().execute.return_value = {"name": "test_file.txt"}

    mock_downloader_instance = MagicMock()
    mock_downloader.return_value = mock_downloader_instance

    buffer = BytesIO()
    mock_downloader_instance.next_chunk.side_effect = [
        (MagicMock(status=200), False),
        (MagicMock(status=200), True),
    ]
    mock_downloader_instance._fd = buffer

    content, filename = download_file("file_id")

    assert filename == "test_file.txt"
    assert content == b""
