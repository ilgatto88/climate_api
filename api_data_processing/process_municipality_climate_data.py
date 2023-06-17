from api_data_processing import (
    config,
    create_data_dictionaries,
    format_conversion,
    process_historical,
    process_oeks,
)
from api_data_processing.models import MunicipalityDataSettings


def create_municipality_climate_data(settings: MunicipalityDataSettings) -> dict:
    meta_dict = create_data_dictionaries.create_municipality_meta_dict(settings)

    historical_dict = create_data_dictionaries.create_historical_data_dict()
    historical_dict["historical"].update(
        process_historical.create_historical_raw_data(settings)
    )
    historical_dict["historical"].update(
        process_historical.create_historical_statistics(settings)
    )

    ensemble_dict = {"ensemble": {}}

    for scenario in ["rcp26", "rcp85"]:
        ensemble_dict["ensemble"].update({scenario: {}})

        ensemble_dict["ensemble"][scenario].update(
            create_data_dictionaries.create_ensemble_data_dict(
                process_oeks.oeks_1d_data_pipeline(settings, scenario)
            )
        )

        ensemble_dict["ensemble"][scenario].update(
            process_oeks.oeks_0d_data_pipeline(settings, scenario)
        )

    climate_data_dict = format_conversion.concatenate_dictionaries(
        [meta_dict, historical_dict, ensemble_dict]
    )

    return climate_data_dict


if __name__ == "__main__":
    municipality_settings = MunicipalityDataSettings(
        municipalityId=10101,
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
    data = create_municipality_climate_data(municipality_settings)
    print(data)
    print("Processing finished.")
