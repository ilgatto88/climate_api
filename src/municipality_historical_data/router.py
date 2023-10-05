from typing import Mapping

from fastapi import APIRouter, Depends, status

from src.auth.bearer import JWTBearer
from src.municipality_historical_data import service
from src.municipality_historical_data.dependencies import (
    municipality_historical_data_exists,
    municipality_historical_data_not_exists,
)
from src.municipality_historical_data.models import MunicipalityHistoricalData

router = APIRouter()


@router.get(
    "/{parameter}/{m_id}",
    name="Get municipality data by ID and climate parameter",
    response_model=MunicipalityHistoricalData,
    status_code=status.HTTP_200_OK,
)
async def get_historical_municipality_data_by_id_and_parameter(
    municipality_data: Mapping = Depends(municipality_historical_data_exists),
) -> Mapping | None:
    """
    Retrieves the historical climate data for a municipality
    from the database based on the given ID and climate parameter.
    """
    return municipality_data


@router.post(
    "/{parameter}/",
    name="Create new historical municipality data for the selected climate parameter",
    response_model=MunicipalityHistoricalData,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
async def post_historical_municipality_data(
    municipality_data: MunicipalityHistoricalData = Depends(
        municipality_historical_data_not_exists
    ),
) -> MunicipalityHistoricalData:
    """
    Creates a new historical municipality data in the database with the provided data
    and returns the created data.
    """
    return await service.create_historical_municipality_data(municipality_data)
