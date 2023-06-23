import json

import pytest

from src.models import MunicipalityData
from src.municipality_data import database as municipality_data_database
from src.tests.conftest import TEST_DATA_PATH


@pytest.mark.anyio
async def test_remove_all_municipality_data():
    await municipality_data_database.remove_all_municipality_data()


@pytest.mark.anyio
async def test_create_municipality_data():
    sample_municipality_data_file_path = (
        f"{TEST_DATA_PATH}/sample_municipality_data.json"
    )
    with open(sample_municipality_data_file_path) as json_file:
        sample_data = json.load(json_file)
        sample_municipality_data = MunicipalityData(**sample_data)
    municipality_data = await municipality_data_database.create_municipality_data(
        sample_municipality_data
    )
    assert municipality_data is not None
    assert municipality_data.meta.municipalityId == 10101


@pytest.mark.anyio
async def test_fetch_municipality_data_by_id():
    municipality_data = await municipality_data_database.fetch_municipality_data_by_id(
        10101
    )
    assert municipality_data is not None
    assert municipality_data["meta"]["municipalityId"] == 10101


@pytest.mark.anyio
async def test_remove_municipality_data_by_id():
    municipality_data = await municipality_data_database.remove_municipality_data_by_id(
        10101
    )
    assert municipality_data is True


@pytest.mark.anyio
async def test_remove_municipality_data_by_id_not_found():
    municipality_data = await municipality_data_database.remove_municipality_data_by_id(
        10101
    )
    assert municipality_data is False
