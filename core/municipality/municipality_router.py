from fastapi import APIRouter, HTTPException

from core.misc_models import Municipality
from core.municipality import municipality_db

router = APIRouter(prefix="/api/municipality", tags=["municipality"])


@router.get("/")
async def get_municipalities() -> list[Municipality]:
    """
    Retrieves all municipalities from the database and
    returns them as a list.
    """
    response = await municipality_db.fetch_all_municipalities()
    return response


@router.get("/{m_id}", response_model=Municipality)
async def get_municipality_by_id(m_id: int) -> Municipality:
    """Retrieves a municipality from the database based on the given ID."""
    response = await municipality_db.fetch_municipality_by_id(m_id)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@router.post("/", response_model=Municipality)
async def post_municipality(municipality: Municipality) -> Municipality:
    """
    Creates a new municipality in the database with the provided data
    and returns the created municipality.
    """
    m_id = municipality.m_id
    municipality_exists = await municipality_db.fetch_municipality_by_id(m_id)
    if municipality_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Municipality with {m_id=} already exists.",
        )

    response = await municipality_db.create_municipality(municipality)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Bad Request")


@router.put("/{m_id}", response_model=Municipality)
async def update_one_municipality(m_id: int, name: str, state: str) -> Municipality:
    """
    Updates the name and state fields of a municipality in the database
    based on the given ID and returns the updated municipality as a response.
    """
    response = await municipality_db.update_municipality(m_id, name, state)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@router.delete("/{m_id}")
async def delete_one_municipality(m_id: int):
    """
    Deletes a municipality from the database based on the given ID.
    Returns a success message if the deletion is successful.
    """
    response = await municipality_db.remove_municipality(m_id)
    if response:
        return f"Successfully deleted municipality with {m_id=}"
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )
