from flask import Blueprint, request, jsonify, Response
from services.drive_service import list_files, upload_file, delete_file, download_file
from logging_module import setup_logger

logger = setup_logger(__name__)  # Initialize logger for this module

file_routes = Blueprint("files", __name__)

@file_routes.route("/files", methods=["GET"])
def get_files():
    """Endpoint to list files."""
    try:
        logger.debug("Request received to list files.")
        files = list_files()
        logger.debug("Files retrieved successfully: %s", files)
        return jsonify({"files": files})
    except Exception as e:
        logger.error("Error retrieving files: %s", e)
        return jsonify({"error": "Failed to retrieve files"}), 500

@file_routes.route("/files/upload", methods=["POST"])
def upload():
    """Endpoint to upload a file."""
    try:
        logger.debug("Request received to upload a file.")
        if "file" not in request.files:
            logger.error("No file part in the request.")
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            logger.error("No selected file.")
            return jsonify({"error": "No file selected"}), 400

        logger.debug("File to be uploaded: %s", file.filename)
        upload_file(file)
        logger.info("File uploaded successfully: %s", file.filename)
        return jsonify({"message": "File uploaded successfully"})
    except Exception as e:
        logger.error("Error uploading file: %s", e)
        return jsonify({"error": "Failed to upload file"}), 500

@file_routes.route("/files/delete/<file_id>", methods=["DELETE"])
def delete(file_id):
    """Endpoint to delete a file."""
    try:
        logger.debug("Request received to delete file with ID: %s", file_id)
        delete_file(file_id)
        logger.info("File deleted successfully: %s", file_id)
        return jsonify({"message": "File deleted successfully"})
    except Exception as e:
        logger.error("Error deleting file with ID %s: %s", file_id, e)
        return jsonify({"error": "Failed to delete file"}), 500

@file_routes.route("/files/download/<file_id>", methods=["GET"])
def download(file_id):
    """Endpoint to download a file."""
    try:
        logger.debug("Request received to download file with ID: %s", file_id)
        file_content, file_name = download_file(file_id)
        
        response = Response(
            file_content,
            headers={
                "Content-Disposition": f"attachment; filename={file_name}",
                "Content-Type": "application/octet-stream",
            },
        )
        logger.info("File downloaded successfully: %s", file_name)
        return response
    except Exception as e:
        logger.error("Error downloading file with ID %s: %s", file_id, e)
        return jsonify({"error": "Failed to download file"}), 500
