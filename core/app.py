from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from core.auth import auth_router
from core.municipality import municipality_router
from core.municipality_data import municipality_data_router

v1_prefix = "/api/v1"
BASE_API_URI = "http://127.0.0.1:8000"

API_NAME = "climATe API"
API_VERSION = "0.2.0"

app = FastAPI(
    title=API_NAME,
    description="Climate data API",
    version=API_VERSION,
)

app.include_router(
    municipality_data_router.router,
    prefix=f"{v1_prefix}/MunicipalityData",
    tags=["MunicipalityData"],
)
app.include_router(
    municipality_router.router,
    prefix=f"{v1_prefix}/Municipalities",
    tags=["Municipalities"],
)
app.include_router(
    auth_router.router,
    prefix="/api/Users",
    tags=["Users"],
)

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


def custom_openapi():
    schemas_to_pop = [
        "MunicipalityDataMeta",
        "MunicipalityDataHistorical",
        "MunicipalityDataRCP",
        "MunicipalityDataEnsemble",
        "MunicipalityDataHistorical",
        "MunicipalityDataMeta",
        "Statistics1D",
        "UserLoginSchema",
        "ValidationError",
        "HTTPValidationError",
    ]

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(title=API_NAME, version=API_VERSION, routes=app.routes)
    for schema in schemas_to_pop:
        openapi_schema["components"]["schemas"].pop(schema, None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
