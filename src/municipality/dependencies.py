from pyparsing import Mapping

from src.municipality import service as municipality_service
from src.municipality.exceptions import MunicipalityAlreadyExists, MunicipalityNotFound
from src.municipality.models import Municipality


async def municipality_exists(m_id: int) -> Mapping | None:
    """Checks if a municipality exists in the database based on the given ID"""
    municipality = await municipality_service.fetch_municipality_by_id(m_id)
    if municipality:
        return municipality
    raise MunicipalityNotFound(m_id)


async def municipality_not_exists(instance: Municipality) -> Municipality | None:
    municipality = await municipality_service.fetch_municipality_by_id(instance.m_id)
    if municipality is None:
        return instance
    raise MunicipalityAlreadyExists(instance.m_id)
