import logging
import traceback
from services.monitoring import capture_exception
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app_errors.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def log_exception(context, exception):
    logging.error(
        "%s | %s | %s",
        context,
        str(exception),
        traceback.format_exc(),
    )

    capture_exception(exception)


def safe_error_message():
    return "An unexpected error occurred. Please try again or contact support if the issue continues."
