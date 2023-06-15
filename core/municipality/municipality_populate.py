import requests

from climate_data_processing import config, geodataframe_tools, static_geo


def populate(m_id: int, name: str, state: str):
    API_URI = "http://127.0.0.1:8000/api/Municipalities/"
    requests.post(
        API_URI,
        json={"m_id": m_id, "name": name, "state": state},
    )


if __name__ == "__main__":
    # Populates database, takes municipality information from shapefile
    shape_data = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)

    counter = 0
    for _, row in shape_data.iterrows():
        m_id, name = row["g_id"], row["g_name"]
        state = static_geo.STATES[m_id[0]]

        populate(m_id, name, state)
        counter += 1

    # add Wien
    populate(90000, "Wien", "Wien")
    counter += 1

    print(f"Added {counter} municipalities to the database.")
