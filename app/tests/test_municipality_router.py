import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

ENDPOINT = "/api/v1/Municipalities"


@pytest.mark.anyio
async def test_get_municipalities(client: AsyncClient, mocker: MockFixture):
    mocker.patch(
        "app.municipality.municipality_db.fetch_all_municipalities",
        return_value=[
            {"m_id": 1, "name": "City 1", "state": "State1"},
            {"m_id": 2, "name": "City 2", "state": "State2"},
        ],
    )
    response = await client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.anyio
async def test_get_municipality_by_id(client: AsyncClient, mocker: MockFixture) -> None:
    mocker.patch(
        "app.municipality.municipality_db.fetch_municipality_by_id",
        return_value={"m_id": 10101, "name": "Eisenstadt", "state": "Burgenland"},
    )
    response = await client.get(f"{ENDPOINT}/10101")
    assert response.status_code == 200
    assert response.json() == {
        "m_id": 10101,
        "name": "Eisenstadt",
        "state": "Burgenland",
    }


@pytest.mark.anyio
async def test_get_municipality_by_id_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture
) -> None:
    mocker.patch(
        "app.municipality.municipality_db.fetch_municipality_by_id",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/00000")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality in the database with m_id=0"
    }
