import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture

from src.municipality.models import Municipality

ENDPOINT = "/api/v1/Municipalities"

municipality_instance_1 = Municipality(m_id=1, name="Test City 1", state="Test State 1")
municipality_instance_1_update = Municipality(
    m_id=1, name="Test City 2", state="Test State 2"
)
municipality_instance_2 = Municipality(m_id=2, name="Test City 2", state="Test State 2")


@pytest.fixture
def mock_jwt_bearer(mocker: MockFixture):
    mocker.patch("src.municipality.router.JWTBearer.__call__", return_value=None)


@pytest.mark.anyio
async def test_post_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    mocker.patch(
        "src.municipality.service.fetch_municipality_by_id",
        return_value=None,
    )
    mocker.patch(
        "src.municipality.service.create_municipality",
        return_value=municipality_instance_1.dict(),
    )
    response = await client.post(ENDPOINT, json=municipality_instance_1.dict())
    assert response.status_code == 201
    assert response.json() == municipality_instance_1.dict()


@pytest.mark.anyio
async def test_post_municipality_which_already_exists(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    mocker.patch(
        "src.municipality.service.fetch_municipality_by_id",
        return_value=municipality_instance_1,
    )
    response = await client.post(ENDPOINT, json=municipality_instance_1.dict())
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            (
                (
                    f"There is already a municipality in the database with "
                    f"m_id={municipality_instance_1.m_id}"
                )
            )
        )
    }


@pytest.mark.anyio
async def test_get_municipalities(client: AsyncClient, mocker: MockFixture):
    mocker.patch(
        "src.municipality.service.fetch_all_municipalities",
        return_value=[municipality_instance_1],
    )
    response = await client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.anyio
async def test_get_municipality_by_id(client: AsyncClient, mocker: MockFixture) -> None:
    mocker.patch(
        "src.municipality.service.fetch_municipality_by_id",
        return_value=municipality_instance_1,
    )
    response = await client.get(f"{ENDPOINT}/1")

    assert response.status_code == 200
    assert response.json() == municipality_instance_1.dict()


@pytest.mark.anyio
async def test_get_municipality_by_id_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture
) -> None:
    mocker.patch(
        "src.municipality.service.fetch_municipality_by_id",
        return_value=None,
    )
    response = await client.get(f"{ENDPOINT}/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality in the database with m_id=0"
    }


@pytest.mark.anyio
async def test_put_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    mocker.patch(
        "src.municipality.service.update_municipality",
        return_value=municipality_instance_1_update.dict(),
    )
    response = await client.put(
        f"{ENDPOINT}/{municipality_instance_1.m_id}",
        json=municipality_instance_1_update.dict(exclude={"m_id"}),
    )
    assert response.status_code == 201
    assert response.json() == municipality_instance_1_update.dict()


@pytest.mark.anyio
async def test_put_municipality_which_doesnt_exist(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    mocker.patch(
        "src.municipality.service.update_municipality",
        return_value=None,
    )
    response = await client.put(
        f"{ENDPOINT}/{municipality_instance_2.m_id}",
        json=municipality_instance_2.dict(exclude={"m_id"}),
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            f"There is no municipality in the database with "
            f"m_id={municipality_instance_2.m_id}"
        )
    }


@pytest.mark.anyio
async def test_delete_municipality(
    client: AsyncClient, mocker: MockFixture, mock_jwt_bearer: None
) -> None:
    mocker.patch(
        "src.municipality.service.remove_municipality",
        return_value=municipality_instance_1_update,
    )
    response = await client.delete(
        f"{ENDPOINT}/{municipality_instance_1_update.m_id}",
    )
    assert response.status_code == 200
    assert response.json() == (
        f"Successfully deleted municipality with "
        f"m_id={municipality_instance_1_update.m_id}"
    )
