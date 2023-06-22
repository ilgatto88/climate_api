import json

import pytest

from app.core.models import MunicipalityData
from app.municipality_data import municipality_data_db
from app.tests.conftest import TEST_DATA_PATH


@pytest.mark.anyio(scope="module")
async def test_create_municipality_data():
    sample_municipality_data_file_path = (
        f"{TEST_DATA_PATH}/sample_municipality_data.json"
    )
    with open(sample_municipality_data_file_path) as json_file:
        sample_data = json.load(json_file)
        sample_municipality_data = MunicipalityData(**sample_data)
    municipality_data = await municipality_data_db.create_municipality_data(
        sample_municipality_data
    )
    assert municipality_data is not None
    assert municipality_data.meta.municipalityId == 10101


@pytest.mark.anyio
async def test_fetch_municipality_data_by_id():
    municipality_data = await municipality_data_db.fetch_municipality_data_by_id(10101)
    assert municipality_data is not None
    assert municipality_data["meta"]["municipalityId"] == 10101


@pytest.mark.anyio
async def test_remove_municipality_data_by_id():
    municipality_data = await municipality_data_db.remove_municipality_data_by_id(10101)
    assert municipality_data is not None
    assert municipality_data["meta"]["municipalityId"] == 10101


@pytest.mark.anyio
async def test_remove_municipality_data_by_id_not_found():
    municipality_data = await municipality_data_db.remove_municipality_data_by_id(10101)
    assert municipality_data is None
