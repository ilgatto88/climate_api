from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.municipality import municipality_router

app = FastAPI(
    title="climATe API",
    description="Climate data API",
    version="0.1.0",
)

app.include_router(municipality_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def index():
    """Redirects the user to the documentation page."""
    return RedirectResponse("docs")
