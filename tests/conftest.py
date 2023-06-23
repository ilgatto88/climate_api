import pytest
from httpx import AsyncClient

from src.main import app

BASE_URL = "http://127.0.0.1:8000"

TEST_DATA_PATH = "tests/data"


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
