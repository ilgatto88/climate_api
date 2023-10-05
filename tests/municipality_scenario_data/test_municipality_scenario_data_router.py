import json

import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

from tests.conftest import TEST_DATA_PATH

ENDPOINT = "/api/v1/municipalitydata/scenario"

MAIN_KEYS = (
    "municipalityId",
    "climateParameter",
    "source",
    "temporalResolution",
    "ensembleTimeRange",
    "modelNames",
    "rawData",
    "statistics0D",
    "statistics1D",
)


@pytest.mark.anyio
async def test_get_municipality_scenario_data_by_id_parameter_and_scenario(
    client: AsyncClient, mocker: MockFixture
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_scenario_data.json"

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "src.municipality_scenario_data.service.fetch_municipality_scenario_data_by_id_parameter_and_scenario",
        return_value=sample_data,
        status_code=200,
    )

    response = await client.get(f"{ENDPOINT}/rcp26/tm/10101")
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert all(key in response.json() for key in MAIN_KEYS)


@pytest.mark.anyio
async def test_get_municipality_scenario_data_by_id_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture
):
    mocker.patch(
        "src.municipality_scenario_data.service.fetch_municipality_scenario_data_by_id_parameter_and_scenario",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/rcp26/tm/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality scenario data in "
        "the database with m_id=0, parameter='tm' and scenario='rcp26'"
    }


@pytest.fixture
def mock_jwt_bearer(mocker: MockFixture):
    mocker.patch(
        "src.municipality_scenario_data.router.JWTBearer.__call__",
        return_value=None,
    )


@pytest.mark.anyio(scope="session")
async def test_post_municipality_scenario_data(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_scenario_data.json"

    mocker.patch(
        "src.municipality_scenario_data.service.fetch_municipality_scenario_data_by_id_parameter_and_scenario",
        return_value=None,
    )

    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    mocker.patch(
        "src.municipality_scenario_data.service.create_municipality_scenario_data",
        return_value=sample_data,
        status_code=201,
    )

    response = await client.post(ENDPOINT, json=sample_data)
    assert response.status_code == 201
    assert type(response.json()) == dict
    assert all(key in response.json() for key in MAIN_KEYS)


@pytest.mark.anyio
async def test_post_municipality_scenario_data_with_existing_m_id(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
):
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipality_scenario_data.json"
    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)

    mocker.patch(
        "src.municipality_scenario_data.service.fetch_municipality_scenario_data_by_id_parameter_and_scenario",
        return_value=sample_data,
    )

    response = await client.post(ENDPOINT, json=sample_data)
    assert response.status_code == 400
    response_text_part1 = "There is already a municipality data "
    response_text_part2 = "document in the database with m_id=10101"
    assert response.json() == {"detail": response_text_part1 + response_text_part2}
