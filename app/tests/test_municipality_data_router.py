import json

import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

ENDPOINT = "/api/v1/MunicipalityData"


@pytest.mark.anyio
async def test_get_municipality_data_by_id(client: AsyncClient, mocker: MockFixture):
    sample_file_path = "app/tests/data/sample_municipality_data.json"
    main_keys = ("meta", "historical", "ensemble")
    meta_keys = (
        "municipalityId",
        "climateParameter",
        "temporalResolution",
        "analysisTimeRange",
        "ensembleTimeRange",
    )

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "app.municipality_data.municipality_data_db.fetch_municipality_data_by_id",
        return_value=sample_data,
        status_code=200,
    )

    response = await client.get(f"{ENDPOINT}/10101")
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert all(key in response.json() for key in main_keys)
    assert all(key in response.json()["meta"] for key in meta_keys)


@pytest.mark.anyio
async def test_get_municipality_data_by_id_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture
):
    mocker.patch(
        "app.municipality_data.municipality_data_db.fetch_municipality_data_by_id",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality data in the database with m_id=0"
    }
