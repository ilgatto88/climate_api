from typing import Any

from src.database import climate_data
from src.municipality_data.models import MunicipalityData

municipality_data_collection = climate_data.MunicipalityData


async def fetch_municipality_data_by_id(m_id: int) -> dict[str, Any] | None:
    """
    Retrieves a municipality data document from the collection based on the given ID.
    """
    document = await municipality_data_collection.find_one(
        {"meta.municipalityId": m_id}
    )
    return document


async def create_municipality_data(
    municipality_data: MunicipalityData,
) -> MunicipalityData:
    """
    Inserts a new municipality data document into the collection
    and returns the created municipality data.
    """
    await municipality_data_collection.insert_one(municipality_data.dict())
    return municipality_data


async def remove_municipality_data_by_id(m_id: int) -> bool:
    """
    Removes a municipality data document from the collection based on the given ID.
    """
    dateled_municipality_data = await municipality_data_collection.delete_one(
        {"meta.municipalityId": m_id}
    )
    if dateled_municipality_data.deleted_count == 1:
        return True
    return False


async def remove_all_municipality_data() -> None:
    """Removes all municipality data documents from the database."""
    x = await municipality_data_collection.delete_many({})
    print(f"Removed all ({x.deleted_count}) municipalities from the database.")
