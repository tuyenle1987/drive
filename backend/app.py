import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_session import Session
from routes.auth_routes import auth_routes
from routes.file_routes import file_routes
from logging_module import setup_logger, correlation_id_var
from config import DevelopmentConfig, ProductionConfig
from correlation import correlation_id_middleware

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
ENV = os.getenv("FLASK_ENV", "development")
if ENV == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Initialize logger
logger = setup_logger("app")
logger.info(f"Running in {ENV} mode.")

# Configure session
Session(app)

# Enable CORS
CORS(app, supports_credentials=True)

# Apply middleware
correlation_id_middleware(app)

@app.before_request
def set_correlation_id_for_logging():
    """Set correlation ID in the logging context."""
    correlation_id = getattr(g, "correlation_id", "N/A")
    correlation_id_var.set(correlation_id)

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(file_routes)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint accessed.")
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    logger.info("Starting Flask app...")
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
