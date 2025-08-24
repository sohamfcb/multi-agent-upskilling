# core/logger_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime, timezone, timedelta

# =========
# Paths
# =========
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

APP_LOG_FILE = LOG_DIR / "app.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"
SQL_LOG_FILE = LOG_DIR / "sqlalchemy.log"

# =========
# Formats
# =========
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(filename)s | %(name)s | "
    "%(funcName)s:%(lineno)d | %(message)s"
)

ACCESS_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

SQL_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# =========
# Formatter with IST timezone
# =========
IST = timezone(timedelta(hours=5, minutes=30))

class ISTFormatter(logging.Formatter):
    """Formatter that emits IST (UTC+5:30) timestamps."""

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=IST)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

# =========
# Handlers
# =========
def _build_console_handler(level=logging.INFO, fmt: str = LOG_FORMAT) -> logging.Handler:
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(level)
    h.setFormatter(ISTFormatter(fmt))
    return h

def _build_rotating_handler(
    file_path: Path,
    level=logging.DEBUG,
    fmt: str = LOG_FORMAT,
    max_bytes: int = 5_000_000,
    backups: int = 5,
) -> logging.Handler:
    h = RotatingFileHandler(
        file_path, maxBytes=max_bytes, backupCount=backups, encoding="utf-8", delay=True
    )
    h.setLevel(level)
    h.setFormatter(ISTFormatter(fmt))
    return h

# =========
# Public API
# =========
def init_logging() -> None:
    """
    Initialize logging for:
      - app.*          -> console + app.log
      - uvicorn.*      -> console + access.log (access) / app.log (error)
      - sqlalchemy.*   -> console + sqlalchemy.log
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    console = _build_console_handler(level=logging.INFO, fmt=LOG_FORMAT)
    app_file = _build_rotating_handler(APP_LOG_FILE, level=logging.DEBUG, fmt=LOG_FORMAT)
    access_file = _build_rotating_handler(ACCESS_LOG_FILE, level=logging.INFO, fmt=ACCESS_FORMAT)
    sql_file = _build_rotating_handler(SQL_LOG_FILE, level=logging.DEBUG, fmt=SQL_FORMAT)

    def _ensure_handler(logger: logging.Logger, handler: logging.Handler):
        if not any(
            isinstance(h, handler.__class__) and getattr(h, "baseFilename", None) == getattr(handler, "baseFilename", None)
            for h in logger.handlers
        ):
            logger.addHandler(handler)

    # ---- app.* (your code)
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = False
    _ensure_handler(app_logger, console)
    _ensure_handler(app_logger, app_file)

    # ---- uvicorn.error
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.setLevel(logging.INFO)
    uvicorn_error.propagate = False
    _ensure_handler(uvicorn_error, console)
    _ensure_handler(uvicorn_error, app_file)

    # ---- uvicorn.access
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.setLevel(logging.INFO)
    uvicorn_access.propagate = False
    _ensure_handler(uvicorn_access, console)
    _ensure_handler(uvicorn_access, access_file)

    # ---- uvicorn general
    uvicorn_general = logging.getLogger("uvicorn")
    uvicorn_general.setLevel(logging.INFO)
    uvicorn_general.propagate = False
    _ensure_handler(uvicorn_general, console)
    _ensure_handler(uvicorn_general, app_file)

    # ---- SQLAlchemy
    sqla_engine = logging.getLogger("sqlalchemy.engine")
    sqla_engine.setLevel(logging.INFO)
    sqla_engine.propagate = False
    _ensure_handler(sqla_engine, console)
    _ensure_handler(sqla_engine, sql_file)

def get_logger(name: str) -> logging.Logger:
    """Get a namespaced app logger: usage -> get_logger("login")"""
    logger = logging.getLogger(f"app.{name}")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if not logger.handlers:
        _ensure_minimal_handlers(logger)
    return logger

def _ensure_minimal_handlers(logger: logging.Logger) -> None:
    console = _build_console_handler(level=logging.INFO, fmt=LOG_FORMAT)
    app_file = _build_rotating_handler(APP_LOG_FILE, level=logging.DEBUG, fmt=LOG_FORMAT)
    if not logger.handlers:
        logger.addHandler(console)
        logger.addHandler(app_file)
