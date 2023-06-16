import logging
import logging.config
import random
import string
import time
from os import path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.auth import auth_router
from core.municipality import municipality_router
from core.municipality_data import municipality_data_router

# setup loggers
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
try:
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
except Exception as e:
    print("Error loading logging configuration:")
    print(e)

logger = logging.getLogger(__name__)

v1_prefix = "/api/v1"
BASE_API_URI = "http://127.0.0.1:8000"

app = FastAPI(
    title="climATe API",
    description="Climate data API",
    version="0.1.0",
)

app.include_router(municipality_data_router.router, prefix=v1_prefix)
app.include_router(municipality_router.router, prefix=v1_prefix)
app.include_router(auth_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index():
    """Redirects the user to the documentation page."""
    return RedirectResponse("/docs")


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
