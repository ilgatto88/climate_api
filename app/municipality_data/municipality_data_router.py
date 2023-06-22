from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth_bearer import JWTBearer
from app.core.models import MunicipalityData
from app.municipality_data import municipality_data_db

router = APIRouter()


@router.get("/{m_id}", response_model=MunicipalityData)
async def get_municipality_data_by_id(m_id: int) -> dict[str, Any]:
    """
    Retrieves the climate data for municipality from the database
    based on the given ID.
    """
    response = await municipality_data_db.fetch_municipality_data_by_id(m_id)
    if response:
        return response
    raise HTTPException(
        status_code=404,
        detail=f"There is no municipality data in the database with {m_id=}",
    )


@router.post(
    "/",
    response_model=MunicipalityData,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def post_municipality_data(
    municipality_data: MunicipalityData,
) -> MunicipalityData:
    """
    Creates a new municipality data in the database with the provided data
    and returns the created municipality data.
    """
    m_id = municipality_data.meta.municipalityId
    municipality_data_exists = await municipality_data_db.fetch_municipality_data_by_id(
        m_id
    )
    if municipality_data_exists:
        raise HTTPException(
            status_code=400,
            detail=f"Municipality data with {m_id=} already exists.",
        )

    response = await municipality_data_db.create_municipality_data(municipality_data)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Bad Request")
