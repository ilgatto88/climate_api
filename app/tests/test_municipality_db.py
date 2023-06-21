# @pytest.mark.anyio
# async def test_fetch_all_municipalities():
#     municipalities = await municipality_db.fetch_all_municipalities()
#     assert len(municipalities) == 2116


# @pytest.mark.anyio
# async def test_fetch_municipality_by_id(mocker: MockFixture):
#     municipality = municipality_db.fetch_municipality_by_id(10101)
#     assert municipality is not None
#     assert municipality["m_id"] == 10101
#     assert municipality["name"] == "Eisenstadt"
#     assert municipality["state"] == "Burgenland"
