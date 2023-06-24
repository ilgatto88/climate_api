from pyparsing import Mapping

from src.municipality_data import service as municipality_data_service
from src.municipality_data.exceptions import (
    MunicipalityDataAlreadyExists,
    MunicipalityDataNotFound,
)
from src.municipality_data.models import MunicipalityData


async def municipality_data_exists(m_id: int) -> Mapping | None:
    """Checks if a municipality exists in the database based on the given ID"""
    municipality = await municipality_data_service.fetch_municipality_data_by_id(m_id)
    if municipality:
        return municipality
    raise MunicipalityDataNotFound(m_id)


async def municipality_data_not_exists(
    instance: MunicipalityData,
) -> MunicipalityData | None:
    municipality_data = await municipality_data_service.fetch_municipality_data_by_id(
        instance.meta.municipalityId
    )
    if municipality_data is None:
        return instance
    raise MunicipalityDataAlreadyExists(instance.meta.municipalityId)
    if municipality_data is None:
        return instance
    raise MunicipalityDataAlreadyExists(instance.meta.municipalityId)
