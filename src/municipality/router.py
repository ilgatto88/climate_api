from typing import Mapping

from fastapi import APIRouter, Depends, status

from src.auth.bearer import JWTBearer
from src.municipality import service as municipality_service
from src.municipality.dependencies import municipality_exists, municipality_not_exists
from src.municipality.exceptions import MunicipalityNotFound
from src.municipality.models import Municipality, MunicipalityUpdate

router = APIRouter()


@router.get("/", name="Get all municipalities", status_code=status.HTTP_200_OK)
async def get_municipalities() -> list[Municipality]:
    """Returns all municipalities in the database"""
    response = await municipality_service.fetch_all_municipalities()
    return response


@router.get(
    "/{m_id}",
    name="Get municipality by ID",
    response_model=Municipality,
    status_code=status.HTTP_200_OK,
)
async def get_municipality_by_id(
    municipality: Mapping = Depends(municipality_exists),
) -> Mapping | None:
    """Returns a municipality based on the given ID"""
    return municipality


@router.post(
    "/",
    name="Create a new municipality",
    response_model=Municipality,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
async def post_municipality(
    municipality: Municipality = Depends(municipality_not_exists),
) -> dict[str, str]:
    """Creates a new municipality in the database"""
    return await municipality_service.create_municipality(municipality)


@router.put(
    "/{m_id}",
    name="Update a municipality",
    response_model=Municipality,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def update_municipality(
    m_id: int,
    update_data: MunicipalityUpdate,
) -> dict[str, str]:
    """Updates a municipality in the database based on the given ID"""
    updated_municipality = await municipality_service.update_municipality(
        m_id, update_data.dict()
    )
    if updated_municipality:
        return updated_municipality
    raise MunicipalityNotFound(m_id)


@router.delete(
    "/{m_id}",
    name="Delete a municipality",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def delete_municipality(m_id: int) -> str:
    """Deletes a municipality in the database based on the given ID"""
    deleted_municipality = await municipality_service.remove_municipality(m_id)
    if deleted_municipality:
        return f"Successfully deleted municipality with {m_id=}"
    raise MunicipalityNotFound(m_id)
