from typing import Any

from src.database import climate_data
from src.municipality_scenario_data.models import MunicipalityScenarioData

municipality_scenario_data_collection = climate_data.MunicipalityDataScenario


async def fetch_municipality_scenario_data_by_id_parameter_and_scenario(
    m_id: int,
    parameter: str,
    scenario: str,
) -> dict[str, Any] | None:
    """
    Retrieves a scenario municipality data document from the
    collection based on the given ID and parameter.
    """
    document = await municipality_scenario_data_collection.find_one(
        {"municipalityId": m_id, "climateParameter": parameter, "source": scenario}
    )
    return document


async def create_scenario_municipality_data(
    data: MunicipalityScenarioData,
) -> MunicipalityScenarioData:
    """
    Inserts a new scenario municipality data document into the collection
    and returns the created data.
    """
    await municipality_scenario_data_collection.insert_one(data.dict())
    return data


async def remove_municipality_data_by_id_parameter_and_scenario(
    m_id: int,
    parameter: str,
    scenario: str,
) -> bool:
    """
    Removes a municipality data document from the collection based on the given ID.
    """
    deleted_municipality_data = await municipality_scenario_data_collection.delete_one(
        {"municipalityId": m_id, "climateParameter": parameter, "source": scenario}
    )
    if deleted_municipality_data.deleted_count == 1:
        return True
    return False


async def remove_all_scenario_municipality_data() -> None:
    """Removes all scenario municipality data documents from the database."""
    x = await municipality_scenario_data_collection.delete_many({})
    print(
        (
            f"Removed all ({x.deleted_count}) scenario municipality "
            f"data from the database."
        )
    )
