import json

import pytest

from src.municipality import service as municipality_service
from src.municipality.models import Municipality
from tests.conftest import TEST_DATA_PATH

municipality_instance_1 = Municipality(
    m_id=99999, name="Test Municipality", state="Test State"
)

municipality_instance_1_update = Municipality(
    m_id=99999, name="Test Municipality 2", state="Test State 2"
)


@pytest.mark.anyio
async def test_create_municipality():
    await municipality_service.create_municipality(municipality_instance_1)
    result = await municipality_service.fetch_municipality_by_id(
        municipality_instance_1.m_id
    )
    assert result is not None
    assert result["m_id"] == municipality_instance_1.m_id
    assert result["name"] == municipality_instance_1.name
    assert result["state"] == municipality_instance_1.state


@pytest.mark.anyio
async def test_fetch_all_municipalities():
    municipalities = await municipality_service.fetch_all_municipalities()
    assert len(municipalities) > 0


@pytest.mark.anyio
async def test_fetch_municipality_by_id():
    test_municipality = Municipality(
        m_id=99999, name="Test Municipality", state="Test State"
    )
    municipality = await municipality_service.fetch_municipality_by_id(99999)
    assert municipality is not None
    municipality.pop("_id")  # type: ignore
    assert municipality == test_municipality.dict()


@pytest.mark.anyio
async def test_update_municipality():
    municipality = await municipality_service.update_municipality(
        m_id=99999, data={"name": "Test Municipality 2", "state": "Test State 2"}
    )
    assert municipality is not None
    assert municipality["name"] == "Test Municipality 2"
    assert municipality["state"] == "Test State 2"


@pytest.mark.anyio
async def test_delete_municipality():
    response = await municipality_service.remove_municipality(99999)
    assert response is True


@pytest.mark.anyio
async def test_delete_municipality_which_doesnt_exist():
    municipality = await municipality_service.remove_municipality(99999)
    assert municipality is False


@pytest.mark.anyio
async def test_delete_all_municipalities():
    await municipality_service.remove_all_municipalities()
    municipalities = await municipality_service.fetch_all_municipalities()
    assert len(municipalities) == 0


@pytest.mark.anyio
async def test_create_many_municipalities():
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipalities.json"
    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    municipalities = await municipality_service.create_many_municipalities(sample_data)
    assert len(municipalities) > 2000
