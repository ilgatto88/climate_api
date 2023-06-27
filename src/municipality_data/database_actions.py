import gc

import requests

from api_data_processing import (
    config,
    geodataframe_tools,
    process_municipality_climate_data,
)
from api_data_processing.loaders import load_dataset
from api_data_processing.models import MunicipalityDataSettings
from src.main import BASE_API_URI


def populate(data: dict, token: str) -> requests.Response:
    API_URI = f"{BASE_API_URI}/api/v1/municipalitydata/"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    return requests.post(API_URI, json=data, headers=headers)


if __name__ == "__main__":
    TOKEN = "mytoken"
    PARAMETER = "tm"
    TEMPORAL_RESOLUTION = "annual"

    municipality_list = requests.get(
        "http://localhost:8000/api/v1/municipalities/"
    ).json()

    shape = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)

    historical_data = load_dataset(
        path=(
            f"{config.BASE_DATA_PATH}climate_data/netcdf/historical/"
            f"spartacus-{PARAMETER}-austria-YS.nc"
        )
    )

    for municipality in municipality_list:
        municipality_settings = MunicipalityDataSettings(
            municipalityId=municipality["m_id"],
            climateParameter=PARAMETER,
            temporal_resolution=TEMPORAL_RESOLUTION,
            analysis_start_year=config.ANALYSIS_START_YEAR,
            analysis_end_year=config.ANALYSIS_END_YEAR,
            ensemble_start_year=config.ENSEMBLE_START_YEAR,
            ensemble_end_year=config.ENSEMBLE_END_YEAR,
            shape=shape,
        )
        print(
            f"Processing {municipality_settings.municipalityId} - "
            f"{municipality_settings.climateParameter} ... ",
            end=" ",
        )
        data = process_municipality_climate_data.create_municipality_climate_data(
            municipality_settings, historical_data
        )
        print("finished, now uploading to database ... ", end=" ")
        response = populate(data, TOKEN)
        if response.status_code != 201:
            print("FAILED.")
            print(
                (
                    f"Status code: {response.status_code}, message: "
                    f"{response.json().get('detail')}"
                )
            )
        else:
            print("DONE.")
        gc.collect()
