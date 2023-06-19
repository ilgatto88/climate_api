import pytest
from httpx import AsyncClient

from app.core.main import app

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/"


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
async def test_get_index_page(client: AsyncClient) -> None:
    response = await client.get(f"{ENDPOINT}")
    assert response.status_code == 200
