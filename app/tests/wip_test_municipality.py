import pytest
from httpx import AsyncClient

from app.core.main import app
from app.municipality import municipality_db

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/api/v1/Municipalities"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app,
        base_url=BASE_URL,
        follow_redirects=True,
    ) as client:
        print("Client is ready")
        yield client


@pytest.mark.anyio
async def test_get_all_municipalities(client: AsyncClient):
    response = await client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json()) > 2000


@pytest.mark.anyio
async def test_get_one_municipality(client: AsyncClient) -> None:
    response = await client.get(f"{ENDPOINT}/10101")
    assert response.status_code == 200
    assert response.json() == {
        "m_id": 10101,
        "name": "Eisenstadt",
        "state": "Burgenland",
    }


@pytest.mark.anyio
async def test_get_not_existing_municipality(client: AsyncClient) -> None:
    response = await client.get(f"{ENDPOINT}/00000")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no municipality in the database with m_id=0"
    }


@pytest.mark.anyio
async def test_fetch_all_municipalities():
    municipalities = await municipality_db.fetch_all_municipalities()
    assert len(municipalities) > 2000


@pytest.mark.anyio
async def test_fetch_one_municipality():
    municipality = await municipality_db.fetch_municipality_by_id(10101)
    assert municipality is not None
    assert municipality["m_id"] == 10101
    assert municipality["name"] == "Eisenstadt"
    assert municipality["state"] == "Burgenland"
