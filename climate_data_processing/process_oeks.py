import pandas as pd
import xarray as xr

from climate_data_processing import (
    area_selection,
    classes,
    config,
    data_statistics,
    general,
    loaders,
)


def oeks_1d_data_pipeline(settings: classes.MunicipalityData) -> pd.DataFrame:
    data = loaders.load_dataset(settings.create_input_file_path())
    area_data = area_selection.reduce_area(
        data, settings.parameter, settings.load_geodataframe()
    )

    columns = data[settings.parameter].realization.values
    index = list(range(config.ENSEMBLE_START_YEAR, config.ENSEMBLE_END_YEAR + 1))
    data_as_dataframe = pd.DataFrame(
        area_data, index=columns, columns=index
    ).transpose()
    return data_statistics.add_oeks_statistics(data_as_dataframe)


def oeks_0d_data_pipeline(settings: classes.MunicipalityData) -> dict[str, float]:
    data = loaders.load_dataset(settings.create_input_file_path())
    area_data = area_selection.reduce_area(
        data, settings.parameter, settings.load_geodataframe()
    )
    statistics_dictionaries = {}
    for period in config.STATISTIC_PERIODS_OEKS:
        period_data = create_oeks_0d_stats(area_data, period[0], period[1])
        statistics_dictionaries.update(period_data)

    return statistics_dictionaries


def create_oeks_0d_stats(data: xr.DataArray, start: str, end: str):
    period_key = f"{start}-{end}"
    stat_dim = "realization"
    rounding_decimals = 1

    period_data = data.sel(time=slice(f"{start}-01-01", f"{end}-01-01"))
    data_1d = general.calculate_along_dimension(period_data, "time", xr.DataArray.mean)

    # calculate statistics
    model_min = data_1d.min(dim=stat_dim, keep_attrs=False, skipna=True)
    model_10percentile = data_1d.quantile(
        q=0.1, dim=stat_dim, keep_attrs=False, skipna=True
    )
    model_mean = data_1d.mean(dim=stat_dim, keep_attrs=False, skipna=True)
    model_median = data_1d.median(dim=stat_dim, keep_attrs=False, skipna=True)
    model_90percentile = data_1d.quantile(
        q=0.9, dim=stat_dim, keep_attrs=False, skipna=True
    )
    model_max = data_1d.max(dim=stat_dim, keep_attrs=False, skipna=True)

    # put values into a dictionary and round them
    statistics = {}
    statistics[period_key] = {}
    statistics[period_key]["minimum"] = float(model_min.values)
    statistics[period_key]["10thPercentile"] = float(model_10percentile.values)
    statistics[period_key]["median"] = float(model_mean.values)
    statistics[period_key]["mean"] = float(model_median.values)
    statistics[period_key]["90thPercentile"] = float(model_90percentile.values)
    statistics[period_key]["maximum"] = float(model_max.values)

    return general.round_dict_values(statistics, rounding_decimals)
