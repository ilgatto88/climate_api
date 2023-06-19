import pytest
from httpx import AsyncClient

from app.core.main import app

# from app.municipality_data import municipality_data_db

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/api/v1/MunicipalityData"


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
async def test_get_data_of_one_municipalities(client: AsyncClient):
    response = await client.get(f"{ENDPOINT}/10101")
    response_json = response.json()
    main_keys = ("meta", "historical", "ensemble")
    meta_keys = (
        "municipalityId",
        "climateParameter",
        "temporalResolution",
        "analysisTimeRange",
        "ensembleTimeRange",
    )
    assert response.status_code == 200
    assert type(response_json) == dict
    assert all(key in response_json for key in main_keys)
    assert all(key in response_json["meta"] for key in meta_keys)
