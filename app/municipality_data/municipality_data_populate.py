import requests

from api_data_processing import config, process_municipality_climate_data
from api_data_processing.models import MunicipalityDataSettings
from app.core.main import BASE_API_URI


def populate(data: dict, token: str):
    API_URI = f"{BASE_API_URI}/api/v1/MunicipalityData/"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    requests.post(API_URI, json=data, headers=headers)


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

    token = "Testtoken"

    print(
        f"Processing {municipality_settings.municipalityId} - "
        f"{municipality_settings.climateParameter} ..."
    )
    data = process_municipality_climate_data.create_municipality_climate_data(
        municipality_settings
    )
    print("Processing finished, now uploading to database ...")
    populate(data, token)
    print("Climate data uploaded to database")
