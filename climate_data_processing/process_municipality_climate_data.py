from climate_data_processing import config
from climate_data_processing.classes import OeksMunicipality1DData
from climate_data_processing.create_data_dictionaries import (
    create_ensemble_data_dict,
    create_historical_data_dict,
    create_municipality_meta_dict,
)
from climate_data_processing.format_conversion import (
    concatenate_dictionaries,
)
from climate_data_processing.process_oeks import (
    oeks_0d_data_pipeline,
    oeks_1d_data_pipeline,
)
from climate_data_processing.process_historical import (
    create_historical_raw_data,
    create_historical_statistics,
)


def create_municipality_climate_data(settings: OeksMunicipality1DData):
    meta_dict = create_municipality_meta_dict(settings)

    historical_dict = create_historical_data_dict()
    historical_dict["historical"].update(create_historical_raw_data(settings))
    historical_dict["historical"].update(create_historical_statistics(settings))

    oeks_1d_model_statistics = oeks_1d_data_pipeline(settings)
    ensemble_dict = create_ensemble_data_dict(oeks_1d_model_statistics)
    ensemble_dict["ensemble"]["modelStatistics0D"] = oeks_0d_data_pipeline(settings)

    climate_data_dict = concatenate_dictionaries(
        [meta_dict, historical_dict, ensemble_dict]
    )

    return climate_data_dict


if __name__ == "__main__":
    municipality_settings = OeksMunicipality1DData(
        municipality_id="10101",
        municipality_name="Eisenstadt",
        municipality_state="Burgenland",
        scenario="rcp26",
        parameter="tm",
        temporal_resolution="annual",
        analysis_start_year=config.ANALYSIS_START_YEAR,
        analysis_end_year=config.ANALYSIS_END_YEAR,
        ensemble_start_year=config.ENSEMBLE_START_YEAR,
        ensemble_end_year=config.ENSEMBLE_END_YEAR,
    )

    print(
        f"Processing {municipality_settings.municipality_name}: "
        f"{municipality_settings.scenario} - {municipality_settings.parameter} ..."
    )
    data = create_municipality_climate_data(municipality_settings)
    print(data)
    print("Processing finished.")
