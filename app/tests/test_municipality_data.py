import json

import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

ENDPOINT = "/api/v1/MunicipalityData"


@pytest.mark.anyio
async def test_get_data_of_one_municipality(mocker: MockFixture):
    with open("app/tests/data/sample_municipality_data.json") as json_file:
        sample_data = json.load(json_file)
    response = mocker.patch(
        "app.municipality_data.municipality_data_db.fetch_municipality_data_by_id",
        return_value=sample_data,
        status_code=200,
    )
    main_keys = ("meta", "historical", "ensemble")
    meta_keys = (
        "municipalityId",
        "climateParameter",
        "temporalResolution",
        "analysisTimeRange",
        "ensembleTimeRange",
    )
    assert response.status_code == 200
    assert type(response.return_value) == dict
    assert all(key in response.return_value for key in main_keys)
    assert all(key in response.return_value["meta"] for key in meta_keys)


@pytest.mark.anyio
async def test_get_data_of_one_municipality_with_wrong_id(client: AsyncClient):
    response = await client.get(f"{ENDPOINT}/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality data in the database with m_id=0"
    }
