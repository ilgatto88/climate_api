from typing import Mapping

from fastapi import APIRouter, Depends, status

from src.auth.bearer import JWTBearer
from src.municipality_scenario_data import service
from src.municipality_scenario_data.dependencies import (
    municipality_scenario_data_exists,
    municipality_scenario_data_not_exists,
)
from src.municipality_scenario_data.models import MunicipalityScenarioData

router = APIRouter()


@router.get(
    "/scenario/{scenario}/{parameter}/{m_id}",
    name="Get municipality data by ID and climate parameter",
    response_model=MunicipalityScenarioData,
    status_code=status.HTTP_200_OK,
)
async def get_scenario_municipality_data_by_id_and_parameter(
    municipality_data: Mapping = Depends(municipality_scenario_data_exists),
) -> Mapping | None:
    """
    Retrieves the scenario climate data for a municipality
    from the database based on the given ID, climate parameter and scenario.
    """
    return municipality_data


@router.post(
    "/scenario/{scenario}/{parameter}/",
    name="Create new municipality data for the selected climate parameter and scenario",
    response_model=MunicipalityScenarioData,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
async def post_scenario_municipality_data(
    municipality_data: MunicipalityScenarioData = Depends(
        municipality_scenario_data_not_exists
    ),
) -> MunicipalityScenarioData:
    """
    Creates a new scenario municipality data in the database with the provided data
    and returns the created data.
    """
    return await service.create_scenario_municipality_data(municipality_data)
