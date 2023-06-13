from database.database import get_database

# from climate_data_processing import config
# from core.models import MunicipalityData
# from climate_data_processing.process_municipality_climate_data import (
#     create_municipality_climate_data,
# )


# collection = db["municipality_data"]

# settings = OeksMunicipality1DData(
#     municipality_id="10101",
#     municipality_name="Eisenstadt",
#     municipality_state="Burgenland",
#     scenario="rcp26",
#     parameter="tm",
#     temporal_resolution="annual",
#     analysis_start_year=config.ANALYSIS_START_YEAR,
#     analysis_end_year=config.ANALYSIS_END_YEAR,
#     ensemble_start_year=config.ENSEMBLE_START_YEAR,
#     ensemble_end_year=config.ENSEMBLE_END_YEAR,
# )

# climate_data_dict = create_municipality_climate_data(settings)

# collection.insert_one(climate_data_dict)


if __name__ == "__main__":
    db = get_database()
