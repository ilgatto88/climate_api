from pyparsing import Mapping

from src.municipality_historical_data import service
from src.municipality_historical_data.exceptions import (
    MunicipalityHistoricalDataAlreadyExists,
    MunicipalityHistoricalDataNotFound,
)
from src.municipality_historical_data.models import MunicipalityHistoricalData


async def municipality_historical_data_exists(
    m_id: int, parameter: str
) -> Mapping | None:
    """Checks if a historical municipality exists in the
    database based on the given ID and parameter"""
    municipality = await service.fetch_municipality_historical_data_by_id_and_parameter(
        m_id, parameter
    )
    if municipality:
        return municipality
    raise MunicipalityHistoricalDataNotFound(m_id, parameter)


async def municipality_historical_data_not_exists(
    instance: MunicipalityHistoricalData,
) -> MunicipalityHistoricalData | None:
    data = await service.fetch_municipality_historical_data_by_id_and_parameter(
        instance.municipalityId, instance.climateParameter
    )
    if data is None:
        return instance
    raise MunicipalityHistoricalDataAlreadyExists(
        instance.municipalityId, instance.climateParameter
    )
