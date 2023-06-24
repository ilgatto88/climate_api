from typing import Mapping

from fastapi import APIRouter, Depends

from src.auth.bearer import JWTBearer
from src.municipality_data import service as municipality_data_service
from src.municipality_data.dependencies import (
    municipality_data_exists,
    municipality_data_not_exists,
)
from src.municipality_data.models import MunicipalityData

router = APIRouter()


@router.get(
    "/{m_id}",
    name="Get municipality data by ID",
    response_model=MunicipalityData,
    status_code=200,
)
async def get_municipality_data_by_id(
    municipality_data: Mapping = Depends(municipality_data_exists),
) -> Mapping | None:
    """
    Retrieves the climate data for a municipality from the database
    based on the given ID.
    """
    return municipality_data


@router.post(
    "/",
    name="Create new municipality data",
    response_model=MunicipalityData,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def post_municipality_data(
    municipality_data: MunicipalityData = Depends(municipality_data_not_exists),
) -> MunicipalityData:
    """
    Creates a new municipality data in the database with the provided data
    and returns the created municipality data.
    """
    return await municipality_data_service.create_municipality_data(municipality_data)
