from typing import Any

from src.database import climate_data
from src.municipality_historical_data.models import MunicipalityHistoricalData

municipality_historical_data_collection = climate_data.MunicipalityHistoricalData


async def fetch_municipality_historical_data_by_id_and_parameter(
    m_id: int,
    parameter: str,
) -> dict[str, Any] | None:
    """
    Retrieves a historical municipality data document from the
    collection based on the given ID and parameter.
    """
    document = await municipality_historical_data_collection.find_one(
        {"municipalityId": m_id, "climateParameter": parameter}
    )
    return document


async def create_historical_municipality_data(
    data: MunicipalityHistoricalData,
) -> MunicipalityHistoricalData:
    """
    Inserts a new historical municipality data document into the collection
    and returns the created data.
    """
    await municipality_historical_data_collection.insert_one(data.dict())
    return data


async def remove_municipality_data_by_id_and_parameter(
    m_id: int,
    parameter: str,
) -> bool:
    """
    Removes a municipality data document from the collection based on the given ID.
    """
    deleted_municipality_data = (
        await municipality_historical_data_collection.delete_one(
            {"municipalityId": m_id, "climateParameter": parameter}
        )
    )
    if deleted_municipality_data.deleted_count == 1:
        return True
    return False


async def remove_all_historical_municipality_data() -> None:
    """Removes all historical municipality data documents from the database."""
    x = await municipality_historical_data_collection.delete_many({})
    print(
        (
            f"Removed all ({x.deleted_count}) historical municipality "
            f"data from the database."
        )
    )
