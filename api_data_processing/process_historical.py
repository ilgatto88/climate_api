import xarray as xr

from api_data_processing import area_selection, config, general
from api_data_processing.loaders import load_dataset
from api_data_processing.models import MunicipalityDataSettings


def create_historical_raw_data(
    settings: MunicipalityDataSettings,
) -> dict[str, list[float]]:
    historical_input_path = settings.create_historical_input_file_path()
    data = load_dataset(path=historical_input_path)
    area_data = area_selection.reduce_area(
        data, settings.climateParameter, settings.load_geodataframe()
    )
    raw_data = [round(float(value), 1) for value in area_data.values]
    return {"rawData": raw_data}


def create_historical_statistics(settings: MunicipalityDataSettings) -> dict[str, dict]:
    historical_input_path = settings.create_historical_input_file_path()
    data = load_dataset(path=historical_input_path)
    area_data = area_selection.reduce_area(
        data, settings.climateParameter, settings.load_geodataframe()
    )

    statistics_dictionaries = {}
    for period in config.STATISTIC_PERIODS_HISTORICAL:
        period_data = create_historical_0d_stats(area_data, period[0], period[1])
        statistics_dictionaries.update(period_data)

    return {"statistics0D": statistics_dictionaries}


def create_historical_0d_stats(data: xr.DataArray, start: str, end: str):
    period_key = f"{start}-{end}"
    rounding_decimals = 1

    period_data = data.sel(time=slice(f"{start}-01-01", f"{end}-01-01"))
    historical_mean = general.calculate_along_dimension(
        period_data, "time", xr.DataArray.mean
    )

    # put values into a dictionary and round them
    statistics = {}
    statistics[period_key] = {}
    statistics[period_key]["mean"] = float(historical_mean.values)

    return general.round_dict_values(statistics, rounding_decimals)
