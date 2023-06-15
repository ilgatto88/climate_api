from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.auth import auth_router
from core.municipality import municipality_router
from core.municipality_data import municipality_data_router

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
