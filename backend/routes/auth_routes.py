from flask import Blueprint, request, redirect, session, jsonify
from services.auth_service import get_auth_url, handle_callback
from logging_module import setup_logger

logger = setup_logger(__name__)  # Initialize logger for this module

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/auth/login", methods=["GET"])
def login():
    """Redirect the user to Google's OAuth 2.0 authorization page."""
    logger.debug("Login route accessed.")
    try:
        auth_url = get_auth_url()
        logger.debug("Redirecting to authorization URL: %s", auth_url)
        return redirect(auth_url)
    except Exception as e:
        logger.error("Error in /auth/login: %s", e)
        return jsonify({"error": "Failed to generate authorization URL"}), 500

@auth_routes.route("/auth/callback", methods=["GET"])
def callback():
    """Handle the OAuth 2.0 callback from Google."""
    logger.debug("Callback route accessed with URL: %s", request.url)
    try:
        return handle_callback(request.url)
    except Exception as e:
        logger.error("Error in /auth/callback: %s", e)
        return jsonify({"error": "Failed to handle callback"}), 500

@auth_routes.route("/auth/status", methods=["GET"])
def auth_status():
    """Check if the user is authenticated."""
    is_authenticated = "credentials" in session
    logger.debug("Authentication status: %s", is_authenticated)
    return jsonify({"isAuthenticated": is_authenticated})

@auth_routes.route("/auth/logout", methods=["POST"])
def logout():
    """Logout the user by clearing the session."""
    session.clear()
    logger.debug("User logged out and session cleared.")
    return jsonify({"message": "Logged out successfully"}), 200
