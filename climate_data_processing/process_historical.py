import xarray as xr

from climate_data_processing import area_selection
from climate_data_processing import config
from climate_data_processing import general
from climate_data_processing.classes import OeksMunicipality1DData
from climate_data_processing.loaders import load_dataset


def create_historical_raw_data(
    settings: OeksMunicipality1DData,
) -> dict[str, list[float]]:
    historical_input_path = (
        f"{config.HISTORICAL_DATA_PATH}spartacus-{settings.parameter}-austria-YS.nc"
    )
    data = load_dataset(path=historical_input_path)
    area_data = area_selection.reduce_area(
        data, settings.parameter, settings.load_geodataframe()
    )
    raw_data = [round(float(value), 1) for value in area_data.values]
    return {"rawData": raw_data}


def create_historical_statistics(settings: OeksMunicipality1DData) -> dict[str, dict]:
    historical_input_path = (
        f"{config.HISTORICAL_DATA_PATH}spartacus-{settings.parameter}-austria-YS.nc"
    )
    data = load_dataset(path=historical_input_path)
    area_data = area_selection.reduce_area(
        data, settings.parameter, settings.load_geodataframe()
    )

    statistics_dictionaries = {}
    for period in config.STATISTIC_PERIODS_HISTORICAL:
        period_data = create_historical_0d_stats(area_data, period[0], period[1])
        statistics_dictionaries.update(period_data)

    return {"analysisStatistics0D": statistics_dictionaries}


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
