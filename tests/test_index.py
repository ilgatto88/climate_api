import pytest
from httpx import AsyncClient

ENDPOINT = "/"


@pytest.mark.anyio
async def test_get_index_page(client: AsyncClient) -> None:
    response = await client.get(f"{ENDPOINT}")
    assert response.status_code == 200
    assert response.status_code == 200
    assert response.status_code == 200
