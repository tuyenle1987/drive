import uuid
from flask import request, g

def generate_correlation_id():
    """Generate a unique correlation ID."""
    return str(uuid.uuid4())

def correlation_id_middleware(app):
    """Middleware to generate and attach a correlation ID to each request."""
    @app.before_request
    def before_request():
        correlation_id = request.headers.get("X-Correlation-ID", generate_correlation_id())
        g.correlation_id = correlation_id

    @app.after_request
    def after_request(response):
        if hasattr(g, "correlation_id"):
            response.headers["X-Correlation-ID"] = g.correlation_id
        return response
