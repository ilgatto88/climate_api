import requests

from climate_data_processing import config, process_municipality_climate_data
from core.models import MunicipalityDataSettings


def populate(data: dict):
    API_URI = "http://127.0.0.1:8000/api/MunicipalityData/"
    requests.post(
        API_URI,
        json=data,
    )


if __name__ == "__main__":
    municipality_settings = MunicipalityDataSettings(
        municipalityId=10201,
        climateParameter="tm",
        temporal_resolution="annual",
        analysis_start_year=config.ANALYSIS_START_YEAR,
        analysis_end_year=config.ANALYSIS_END_YEAR,
        ensemble_start_year=config.ENSEMBLE_START_YEAR,
        ensemble_end_year=config.ENSEMBLE_END_YEAR,
    )

    print(
        f"Processing {municipality_settings.municipalityId} - "
        f"{municipality_settings.climateParameter} ..."
    )
    data = process_municipality_climate_data.create_municipality_climate_data(
        municipality_settings
    )
    print("Processing finished, now uploading to database ...")
    populate(data)
    print("Climate data uploaded to database")
