import logging
from contextvars import ContextVar
from config import Config

# Context variable for correlation ID
correlation_id_var = ContextVar("correlation_id", default="N/A")

def setup_logger(name):
    """Set up a logger with correlation ID support."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s [Correlation-ID: %(correlation_id)s]: %(message)s"
    )

    # Add correlation ID to log records
    class CorrelationIDFilter(logging.Filter):
        def filter(self, record):
            record.correlation_id = correlation_id_var.get()
            return True

    logger.addFilter(CorrelationIDFilter())

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger
