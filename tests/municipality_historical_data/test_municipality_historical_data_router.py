import json

import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

from tests.conftest import TEST_DATA_PATH

ENDPOINT = "/api/v1/municipalitydata/historical"

MAIN_KEYS = (
    "municipalityId",
    "climateParameter",
    "source",
    "temporalResolution",
    "analysisTimeRange",
    "rawData",
    "statistics0D",
)


@pytest.mark.anyio
async def test_get_municipality_historical_data_by_id_and_parameter(
    client: AsyncClient, mocker: MockFixture
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_historical_data.json"

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "src.municipality_historical_data.service.fetch_municipality_historical_data_by_id_and_parameter",
        return_value=sample_data,
        status_code=200,
    )

    response = await client.get(f"{ENDPOINT}/tm/10101")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert all(key in response.json() for key in MAIN_KEYS)


@pytest.mark.anyio
async def test_get_municipality_historical_data_by_id_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture
):
    mocker.patch(
        "src.municipality_historical_data.service.fetch_municipality_historical_data_by_id_and_parameter",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/tm/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no historical municipality data "
        "in the database with m_id=0 and parameter='tm'"
    }


@pytest.fixture
def mock_jwt_bearer(mocker: MockFixture):
    mocker.patch(
        "src.municipality_historical_data.router.JWTBearer.__call__",
        return_value=None,
    )


@pytest.mark.anyio(scope="session")
async def test_post_municipality_historical_data(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_historical_data.json"

    mocker.patch(
        "src.municipality_historical_data.service.fetch_municipality_historical_data_by_id_and_parameter",
        return_value=None,
    )

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "src.municipality_historical_data.service.create_historical_municipality_data",
        return_value=sample_data,
        status_code=201,
    )

    response = await client.post(f"{ENDPOINT}/tm/", json=sample_data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert all(key in response.json() for key in MAIN_KEYS)


@pytest.mark.anyio
async def test_post_municipality_historical_data_with_existing_m_id(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_historical_data.json"
    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)

    mocker.patch(
        "src.municipality_historical_data.service.fetch_municipality_historical_data_by_id_and_parameter",
        return_value=sample_data,
    )

    response = await client.post(f"{ENDPOINT}/tm/", json=sample_data)
    assert response.status_code == 400
    response_text_part1 = "There is already a historical municipality data "
    response_text_part2 = "document in the database with m_id=10101 and parameter='tm'"
    assert response.json() == {"detail": response_text_part1 + response_text_part2}
