import pytest

from app.municipality import municipality_db


@pytest.mark.anyio
async def test_fetch_all_municipalities():
    municipalities = await municipality_db.fetch_all_municipalities()
    assert len(municipalities) == 2116


# @pytest.mark.anyio
# async def test_fetch_one_municipality(mocker: MockFixture):
#     municipality = mocker.patch(
#         "app.municipality.municipality_db.fetch_municipality_by_id",
#         return_value={"m_id": 10101, "name": "Eisenstadt", "state": "Burgenland"},
#     )
#     assert municipality.return_value["m_id"] == 10101
#     assert municipality.return_value["name"] == "Eisenstadt"
#     assert municipality.return_value["state"] == "Burgenland"
