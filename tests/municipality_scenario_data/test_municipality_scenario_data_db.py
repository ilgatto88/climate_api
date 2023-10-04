import json

import pytest

from src.municipality_scenario_data import service
from src.municipality_scenario_data.models import MunicipalityScenarioData
from tests.conftest import TEST_DATA_PATH


@pytest.mark.anyio
async def test_remove_all_scenario_municipality_data():
    await service.remove_all_scenario_municipality_data()


@pytest.mark.anyio
async def test_create_municipality_data():
    sample_municipality_data_file_path = (
        f"{TEST_DATA_PATH}/sample_municipality_scenario_data.json"
    )
    with open(sample_municipality_data_file_path) as json_file:
        data = json.load(json_file)
        sample_data = MunicipalityScenarioData(**data)
    municipality_data = await service.create_scenario_municipality_data(sample_data)
    assert municipality_data is not None
    assert municipality_data.municipalityId == 10101
    assert municipality_data.climateParameter == "tm"


@pytest.mark.anyio
async def test_fetch_municipality_scenario_data_by_id_parameter_and_scenario():
    municipality_data = (
        await service.fetch_municipality_scenario_data_by_id_parameter_and_scenario(
            10101, "tm", "rcp26"
        )
    )
    assert municipality_data is not None
    assert municipality_data["municipalityId"] == 10101
    assert municipality_data["climateParameter"] == "tm"
    assert municipality_data["source"] == "rcp26"


@pytest.mark.anyio
async def test_remove_municipality_scenario_data_by_id_parameter_and_scenario():
    municipality_data = (
        await service.remove_municipality_data_by_id_parameter_and_scenario(
            10101, "tm", "rcp26"
        )
    )
    assert municipality_data is True


@pytest.mark.anyio
async def test_remove_municipality_scenario_data_by_id_parameter_and_scenario_not_found():
    municipality_data = (
        await service.remove_municipality_data_by_id_parameter_and_scenario(
            10101, "tm", "rcp26"
        )
    )
    assert municipality_data is False
