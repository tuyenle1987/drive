import os
import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from flask import session
from werkzeug.utils import secure_filename
from googleapiclient.http import MediaIoBaseDownload
from logging_module import setup_logger

logger = setup_logger(__name__)  # Initialize logger for this module

def get_drive_service():
    """Initialize and return the Google Drive API service."""
    if "credentials" not in session:
        logger.error("No credentials found in session.")
        return None

    try:
        # Safely parse credentials from session
        credentials_info = json.loads(session["credentials"])
        
        # Convert parsed credentials into a Credentials object
        credentials = Credentials.from_authorized_user_info(credentials_info)
        
        # Build the Google Drive service
        service = build("drive", "v3", credentials=credentials)
        logger.debug("Google Drive service initialized with credentials.")
        return service
    except json.JSONDecodeError as e:
        logger.error("Failed to parse credentials: %s", e)
    except Exception as e:
        logger.error("Failed to initialize Google Drive service: %s", e)
    
    return None

def list_files():
    """List files from Google Drive."""
    service = get_drive_service()
    if not service:
        logger.error("Google Drive service is not initialized.")
        return []

    try:
        results = service.files().list(pageSize=10, fields="files(id, name, mimeType)").execute()
        files = results.get("files", [])
        logger.debug("Files retrieved successfully: %s", files)
        return files
    except Exception as e:
        logger.error("Error listing files: %s", e)
        return []

def upload_file(file):
    """Upload a file to Google Drive."""
    service = get_drive_service()
    if not service:
        logger.error("Google Drive service is not initialized.")
        raise Exception("Google Drive service is not initialized.")

    try:
        # Save the uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_filepath = os.path.join("/tmp", filename)
        file.save(temp_filepath)
        logger.debug("File saved temporarily at: %s", temp_filepath)

        # Prepare file metadata and media upload
        file_metadata = {"name": filename}
        media = MediaFileUpload(temp_filepath, resumable=True)
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        # Remove temporary file
        os.remove(temp_filepath)
        logger.info("File uploaded successfully: %s", uploaded_file.get("id"))
        return uploaded_file.get("id")
    except Exception as e:
        logger.error("Error uploading file: %s", e)
        raise

def download_file(file_id):
    """Download a file from Google Drive."""
    service = get_drive_service()
    if not service:
        raise Exception("Google Drive service is not initialized.")

    try:
        request = service.files().get_media(fileId=file_id)
        file_metadata = service.files().get(fileId=file_id, fields="name").execute()
        file_name = file_metadata.get("name", "unknown")

        logger.debug("Downloading file: %s", file_name)

        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.debug("Download progress: %d%%", int(status.progress() * 100))

        buffer.seek(0)  # Rewind buffer
        return buffer.read(), file_name
    except Exception as e:
        logger.error("Error downloading file with ID %s: %s", file_id, e)
        raise

def delete_file(file_id):
    """Delete a file from Google Drive."""
    service = get_drive_service()
    if not service:
        logger.error("Google Drive service is not initialized.")
        raise Exception("Google Drive service is not initialized.")

    try:
        service.files().delete(fileId=file_id).execute()
        logger.info("File deleted successfully: %s", file_id)
    except Exception as e:
        logger.error("Error deleting file: %s", e)
        raise
