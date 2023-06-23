from fastapi import APIRouter, Depends, HTTPException

from src.auth.bearer import JWTBearer
from src.municipality import service as municipality_service
from src.municipality.models import Municipality

router = APIRouter()


@router.get("/", name="Get all municipalities")
async def get_municipalities() -> list[Municipality]:
    """
    Retrieves all municipalities from the database and
    returns them as a list.
    """
    response = await municipality_service.fetch_all_municipalities()
    return response


@router.get("/{m_id}", response_model=Municipality)
async def get_municipality_by_id(m_id: int) -> dict[str, str]:
    """Retrieves a municipality from the database based on the given ID."""
    response = await municipality_service.fetch_municipality_by_id(m_id)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@router.post(
    "/",
    response_model=Municipality,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def post_municipality(municipality: Municipality) -> Municipality:
    """
    Creates a new municipality in the database with the provided data
    and returns the created municipality.
    """
    m_id = municipality.m_id
    municipality_exists = await municipality_service.fetch_municipality_by_id(m_id)
    if municipality_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Municipality with {m_id=} already exists.",
        )

    response = await municipality_service.create_municipality(municipality)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Bad Request")


@router.put(
    "/{m_id}",
    response_model=Municipality,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def update_one_municipality(m_id: int, name: str, state: str) -> dict[str, str]:
    """
    Updates the name and state fields of a municipality in the database
    based on the given ID and returns the updated municipality as a response.
    """
    response = await municipality_service.update_municipality(m_id, name, state)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )


@router.delete("/{m_id}", dependencies=[Depends(JWTBearer())])
async def delete_one_municipality(m_id: int) -> str:
    """
    Deletes a municipality from the database based on the given ID.
    Returns a success message if the deletion is successful.
    """
    response = await municipality_service.remove_municipality(m_id)
    if response:
        return f"Successfully deleted municipality with {m_id=}"
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality in the database with {m_id=}",
    )
