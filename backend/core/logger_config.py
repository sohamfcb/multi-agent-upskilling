import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Log file path
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)   # create logs/ if not exists
LOG_FILE = LOG_DIR / "app.log"

# Global log formatter
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(filename)s | %(name)s | "
    "%(funcName)s:%(lineno)d | %(message)s"
)

def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with both console + file handlers."""

    logger = logging.getLogger(name)

    if logger.hasHandlers():  # avoid adding duplicate handlers in reloads
        return logger

    logger.setLevel(logging.DEBUG)  # capture everything, filter at handler

    # --- Console Handler (for dev)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # INFO and above go to console
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # --- File Handler (rotating logs)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # log EVERYTHING to file
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
