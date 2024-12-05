from config import Config
from google_auth_oauthlib.flow import Flow
from flask import session, redirect
from logging_module import setup_logger

logger = setup_logger(__name__)  # Initialize logger for this module

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def create_flow():
    """Create and return a Google OAuth 2.0 flow object."""
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        logger.error("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set.")
        raise EnvironmentError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set.")

    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": Config.GOOGLE_CLIENT_ID,
                    "client_secret": Config.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [Config.REDIRECT_URI],
                }
            },
            scopes=SCOPES,
        )
        flow.redirect_uri = Config.REDIRECT_URI
        logger.debug("OAuth flow created successfully with redirect URI: %s", Config.REDIRECT_URI)
        return flow
    except Exception as e:
        logger.error("Failed to create OAuth flow: %s", e)
        raise

def get_auth_url():
    """Generate and return the Google OAuth 2.0 authorization URL."""
    try:
        flow = create_flow()
        auth_url, _ = flow.authorization_url(prompt="consent")
        logger.debug("Authorization URL generated: %s", auth_url)
        return auth_url
    except Exception as e:
        logger.error("Error generating authorization URL: %s", e)
        raise

def handle_callback(url):
    """Handle the callback from Google OAuth 2.0."""
    logger.debug("Handling callback with URL: %s", url)
    try:
        flow = create_flow()
        flow.fetch_token(authorization_response=url)
        session["credentials"] = flow.credentials.to_json()
        return redirect("http://localhost:3000")
    except Exception as e:
        logger.error("Error handling callback: %s", e)
        raise
