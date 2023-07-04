import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.app_logging.custom_logging import CustomizeLogger
from src.auth import router as auth_router
from src.municipality import router as municipality_router
from src.municipality_data import router as municipality_data_router

logger = logging.getLogger(__name__)
logconfig_path = Path(__file__).parents[0] / "app_logging" / "logging_config.json"

V1_PREFIX = "/api/v1"
BASE_API_URI = "http://127.0.0.1:8000"
API_NAME = "climATe API"
API_VERSION = "0.3.0"


def create_app() -> FastAPI:
    app = FastAPI(
        title=API_NAME,
        description="Climate data API",
        version=API_VERSION,
        debug=False,
    )
    logger = CustomizeLogger.make_logger(logconfig_path)
    app.logger = logger  # type: ignore

    return app


app = create_app()

app.include_router(
    municipality_data_router.router,
    prefix=f"{V1_PREFIX}/municipalitydata",
    tags=["Municipality Data"],
)
app.include_router(
    municipality_router.router,
    prefix=f"{V1_PREFIX}/municipalities",
    tags=["Municipalities"],
)
app.include_router(
    auth_router.router,
    prefix="/api/Users",
    tags=["Users"],
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.get("/", include_in_schema=False)
async def index():
    """Redirects the user to the documentation page."""
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, access_log=True)
