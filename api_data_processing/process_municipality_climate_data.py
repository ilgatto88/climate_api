import time

import xarray as xr

from api_data_processing import (
    config,
    create_data_dictionaries,
    format_conversion,
    geodataframe_tools,
    process_ensemble,
    process_historical,
)
from api_data_processing.loaders import load_dataset
from api_data_processing.models import MunicipalityDataSettings


def create_municipality_climate_data(
    settings: MunicipalityDataSettings, historical_data: xr.Dataset
) -> dict:
    area_geodataframe = settings.load_geodataframe()

    # Meta data
    meta_dict = create_data_dictionaries.create_municipality_meta_dict(settings)

    # Historical data
    preprocessed_historical_data = process_historical.preprocess_historical_data(
        historical_data, settings, area_geodataframe
    )

    historical_dict = create_data_dictionaries.create_historical_data_dict()
    historical_dict["historical"].update(
        process_historical.create_historical_raw_data(preprocessed_historical_data)
    )
    historical_dict["historical"].update(
        process_historical.create_historical_statistics(preprocessed_historical_data)
    )

    # Ensemble data
    ensemble_dict = {"ensemble": {}}

    for scenario in ["rcp26", "rcp85"]:
        preprocessed_ensemble_data = process_ensemble.preprocess_ensemble_data(
            settings, scenario, area_geodataframe
        )
        ensemble_dict["ensemble"].update({scenario: {}})

        ensemble_dict["ensemble"][scenario].update(
            create_data_dictionaries.create_ensemble_data_dict(
                process_ensemble.oeks_1d_data_pipeline(preprocessed_ensemble_data)
            )
        )

        ensemble_dict["ensemble"][scenario].update(
            process_ensemble.oeks_0d_data_pipeline(preprocessed_ensemble_data)
        )

    climate_data_dict = format_conversion.concatenate_dictionaries(
        [meta_dict, historical_dict, ensemble_dict]
    )

    return climate_data_dict


if __name__ == "__main__":
    start_time = time.time()

    shape = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
    municipality_settings = MunicipalityDataSettings(
        municipalityId=10101,
        climateParameter="tm",
        temporal_resolution="annual",
        analysis_start_year=config.ANALYSIS_START_YEAR,
        analysis_end_year=config.ANALYSIS_END_YEAR,
        ensemble_start_year=config.ENSEMBLE_START_YEAR,
        ensemble_end_year=config.ENSEMBLE_END_YEAR,
        shape=shape,
    )

    print(
        f"Processing {municipality_settings.municipalityId} - "
        f"{municipality_settings.climateParameter} ..."
    )

    historical_input_path = (
        f"{config.BASE_DATA_PATH}climate_data/netcdf/historical/"
        f"spartacus-{municipality_settings.climateParameter}-austria-YS.nc"
    )
    historical_data = load_dataset(path=historical_input_path)

    data = create_municipality_climate_data(municipality_settings, historical_data)
    end_time = time.time()
    print("Processing finished.")
    print(f"Time elapsed: {(end_time - start_time)} seconds.")
