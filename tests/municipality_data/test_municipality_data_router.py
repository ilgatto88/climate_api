import json

import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

from tests.conftest import TEST_DATA_PATH

ENDPOINT = "/api/v1/municipalitydata"


@pytest.mark.anyio
async def test_get_municipality_data_by_id(client: AsyncClient, mocker: MockFixture):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_data.json"
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
        "src.municipality_data.service.fetch_municipality_data_by_id",
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
        "src.municipality_data.service.fetch_municipality_data_by_id",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality data in the database with m_id=0"
    }


@pytest.fixture
def mock_jwt_bearer(mocker: MockFixture):
    mocker.patch(
        "src.municipality_data.router.JWTBearer.__call__",
        return_value=None,
    )


@pytest.mark.anyio(scope="session")
async def test_post_municipality_data(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_data.json"
    main_keys = ("meta", "historical", "ensemble")
    meta_keys = (
        "municipalityId",
        "climateParameter",
        "temporalResolution",
        "analysisTimeRange",
        "ensembleTimeRange",
    )

    mocker.patch(
        "src.municipality_data.service.fetch_municipality_data_by_id",
        return_value=None,
    )

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "src.municipality_data.service.create_municipality_data",
        return_value=sample_data,
        status_code=201,
    )

    response = await client.post(ENDPOINT, json=sample_data)
    assert response.status_code == 201
    assert type(response.json()) == dict
    assert all(key in response.json() for key in main_keys)
    assert all(key in response.json()["meta"] for key in meta_keys)


@pytest.mark.anyio
async def test_post_municipality_data_with_existing_m_id(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_data.json"
    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)

    mocker.patch(
        "src.municipality_data.service.fetch_municipality_data_by_id",
        return_value=sample_data,
    )

    response = await client.post(ENDPOINT, json=sample_data)
    assert response.status_code == 400
    response_text_part1 = "There is already a municipality data "
    response_text_part2 = "document in the database with m_id=10101"
    assert response.json() == {"detail": response_text_part1 + response_text_part2}
