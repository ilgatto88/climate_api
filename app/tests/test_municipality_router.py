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


@pytest.fixture
def mock_jwt_bearer(mocker: MockFixture):
    mocker.patch(
        "app.municipality.municipality_router.JWTBearer.__call__", return_value=None
    )


@pytest.mark.anyio(scope="session")
async def test_post_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    ID = 99999
    NAME = "Test City 1"
    STATE = "Test State 1"
    mocker.patch(
        "app.municipality.municipality_db.fetch_municipality_by_id",
        return_value=None,
    )
    mocker.patch(
        "app.municipality.municipality_db.create_municipality",
        return_value={"m_id": ID, "name": NAME, "state": STATE},
    )
    response = await client.post(
        ENDPOINT,
        json={"m_id": ID, "name": NAME, "state": STATE},
    )
    assert response.status_code == 201
    assert response.json() == {
        "m_id": ID,
        "name": NAME,
        "state": STATE,
    }


@pytest.mark.anyio
async def test_post_municipality_which_already_exists(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    ID = 99999
    NAME = "Test City 1"
    STATE = "Test State 1"
    mocker.patch(
        "app.municipality.municipality_db.fetch_municipality_by_id",
        return_value={"m_id": ID, "name": NAME, "state": STATE},
    )
    response = await client.post(
        ENDPOINT,
        json={"m_id": ID, "name": NAME, "state": STATE},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": f"Municipality with m_id={ID} already exists."}


@pytest.mark.anyio
async def test_update_one_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    ID = 99999
    NAME = "Test City 2"
    STATE = "Test State 2"

    mocker.patch(
        "app.municipality.municipality_db.update_municipality",
        return_value={"m_id": ID, "name": NAME, "state": STATE},
    )
    response = await client.put(
        f"{ENDPOINT}/{ID}",
        params={
            "m_id": ID,
            "name": NAME,
            "state": STATE,
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "m_id": ID,
        "name": NAME,
        "state": STATE,
    }


@pytest.mark.anyio
async def test_update_one_municipality_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    ID = 99999
    NAME = "Test City 2"
    STATE = "Test State 2"

    mocker.patch(
        "app.municipality.municipality_db.update_municipality",
        return_value=None,
    )
    response = await client.put(
        f"{ENDPOINT}/{ID}",
        params={
            "m_id": ID,
            "name": NAME,
            "state": STATE,
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"There is no municipality in the database with m_id={ID}"
    }


@pytest.mark.anyio
async def test_delete_one_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    ID = 99999
    NAME = "Test City 1"
    STATE = "Test State 1"

    mocker.patch(
        "app.municipality.municipality_db.remove_municipality",
        return_value={"m_id": ID, "name": NAME, "state": STATE},
    )
    response = await client.delete(
        f"{ENDPOINT}/{ID}",
    )
    assert response.status_code == 200
    assert response.json() == f"Successfully deleted municipality with m_id={ID}"
