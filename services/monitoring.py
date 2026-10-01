import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        traces_sample_rate=0.1,
        send_default_pii=False,
    )


def capture_exception(error):
    if SENTRY_DSN:
        sentry_sdk.capture_exception(error)
