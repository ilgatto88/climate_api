import requests

from api_data_processing import config, geodataframe_tools, static_geo
from app.core.app import BASE_API_URI


def populate(m_id: int, name: str, state: str, token: str):
    API_URI = f"{BASE_API_URI}/api/v1/Municipalities/"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    requests.post(
        API_URI, json={"m_id": m_id, "name": name, "state": state}, headers=headers
    )


if __name__ == "__main__":
    # Populates database, takes municipality information from shapefile
    token = "Testtoken"
    shape_data = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)

    counter = 0
    for _, row in shape_data.iterrows():
        m_id, name = row["g_id"], row["g_name"]
        state = static_geo.STATES[m_id[0]]

        populate(m_id, name, state, token)
        counter += 1

    # add Wien
    populate(90000, "Wien", "Wien", token)
    counter += 1

    print(f"Added {counter} municipalities to the database.")
