from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core import database
from core.models import Municipality

app = FastAPI(
    title="climATe API",
    description="Climate data API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    """Redirects the user to the documentation page."""
    return RedirectResponse("docs")


@app.get("/api/municipality")
async def get_municipalities() -> list[Municipality]:
    """
    Retrieves all municipalities from the database and
    returns them as a list.
    """
    response = await database.fetch_all_municipalities()
    return response


@app.get("/api/municipality/{m_id}", response_model=Municipality)
async def get_municipality_by_id(m_id: int) -> Municipality:
    """Retrieves a municipality from the database based on the given ID."""
    response = await database.fetch_municipality_by_id(m_id)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@app.post("/api/municipality", response_model=Municipality)
async def post_municipality(municipality: Municipality) -> Municipality:
    """
    Creates a new municipality in the database with the provided data
    and returns the created municipality.
    """
    m_id = municipality.m_id
    municipality_exists = await database.fetch_municipality_by_id(m_id)
    if municipality_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Municipality with {m_id=} already exists.",
        )

    response = await database.create_municipality(municipality)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Bad Request")


@app.put("/api/municipality/{m_id}", response_model=Municipality)
async def update_one_municipality(m_id: int, name: str, state: str) -> Municipality:
    """
    Updates the name and state fields of a municipality in the database
    based on the given ID and returns the updated municipality as a response.
    """
    response = await database.update_municipality(m_id, name, state)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@app.delete("/api/municipality/{m_id}")
async def delete_one_municipality(m_id: int):
    """
    Deletes a municipality from the database based on the given ID.
    Returns a success message if the deletion is successful.
    """
    response = await database.remove_municipality(m_id)
    if response:
        return f"Successfully deleted municipality with {m_id=}"
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )
