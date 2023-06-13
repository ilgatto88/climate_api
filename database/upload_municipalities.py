from core.models import Municipality
from climate_data_processing import config, geodataframe_tools


# to execute this script, use ./manage.py shell < preprocessing/upload_municipalities.py
def upload_municipalities_to_db():
    """
    This function uploads the municipalities from a shapefile to the database.
    """
    shape_data = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
    for _, row in shape_data.iterrows():
        print(row["g_id"], row["g_name"])
        Municipality(
            m_id=row["g_id"],
            name=row["g_name"],
            state="",
        )


def upload_vienna_to_db():
    """This function adds Wien to the database."""
    Municipality(m_id=90000, name="Wien", state="")
    print("Wien uploaded to the database.")


upload_municipalities_to_db()
upload_vienna_to_db()
