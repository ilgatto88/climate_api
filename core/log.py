import logging
import logging.config
import random
import string
import time
from os import path

from fastapi import Request

from core.app import app

# setup loggers
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
try:
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
except Exception as e:
    print("Error loading logging configuration:")
    print(e)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        (
            f"rid={idem} completed_in={formatted_process_time}ms "
            f"status_code={response.status_code}"
        )
    )

    return response
