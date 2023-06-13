import datetime
import pandas as pd

from climate_data_processing import config
from climate_data_processing.classes import OeksMunicipality1DData
from climate_data_processing.general import prepare_array_for_json


def create_municipality_meta_dict(meta: OeksMunicipality1DData) -> dict:
    return {
        "meta": {
            "municipalityId": meta.municipality_id,
            "municipalityName": meta.municipality_name,
            "municipalityState": meta.municipality_state,
            "scenario": meta.scenario,
            "parameter": meta.parameter,
            "timeResolution": meta.temporal_resolution,
            "analysisTimeRange": list(
                range(meta.analysis_start_year, meta.analysis_end_year + 1)
            ),
            "ensembleTimeRange": list(
                range(meta.ensemble_start_year, meta.ensemble_end_year + 1)
            ),
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    }


def create_historical_data_dict() -> dict:
    return {"historical": {"analysisName": "Spartacus"}}


def create_ensemble_data_dict(data: pd.DataFrame) -> dict:
    models = [x for x in data if x not in config.STATISTICS + ["Year"]]
    model_raw_data = {}
    for model in models:
        model_raw_data[model] = prepare_array_for_json(data[model])
    return {
        "ensemble": {
            "modelNames": models,
            "modelRawData": model_raw_data,
            "modelStatistics1D": {
                "minimum": prepare_array_for_json(data["Model_minimum"]),
                "10thPercentile": prepare_array_for_json(data["Model_10percentile"]),
                "median": prepare_array_for_json(data["Model_median"]),
                "mean": prepare_array_for_json(data["Model_mean"]),
                "90thPercentile": prepare_array_for_json(data["Model_90percentile"]),
                "maximum": prepare_array_for_json(data["Model_maximum"]),
            },
        }
    }
