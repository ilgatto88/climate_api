from pyparsing import Mapping

from src.municipality_scenario_data import service
from src.municipality_scenario_data.exceptions import (
    MunicipalityScenarioDataAlreadyExists,
    MunicipalityScenarioDataNotFound,
)
from src.municipality_scenario_data.models import MunicipalityScenarioData


async def municipality_scenario_data_exists(
    m_id: int, parameter: str, scenario: str
) -> Mapping | None:
    """Checks if a scenario municipality exists in the
    database based on the given ID and parameter"""
    municipality = (
        await service.fetch_municipality_scenario_data_by_id_parameter_and_scenario(
            m_id, parameter, scenario
        )
    )
    if municipality:
        return municipality
    raise MunicipalityScenarioDataNotFound(m_id, parameter, scenario)


async def municipality_scenario_data_not_exists(
    instance: MunicipalityScenarioData,
) -> MunicipalityScenarioData | None:
    data = await service.fetch_municipality_scenario_data_by_id_parameter_and_scenario(
        instance.municipalityId, instance.climateParameter, instance.source
    )
    if data is None:
        return instance
    raise MunicipalityScenarioDataAlreadyExists(
        instance.municipalityId, instance.climateParameter, instance.source
    )
