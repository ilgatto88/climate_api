import geopandas as gpd
import rioxarray  # pylint: disable=unused-import
import xarray as xr

from climate_data_processing.general import calculate_along_dimension


def clip_dataset(dataset: xr.Dataset, area: gpd.GeoDataFrame) -> xr.Dataset:
    """Clips the dataset using the geometry of a GeoDataFrame and returns the clipped dataset."""
    return dataset.rio.clip(area.geometry)


def clip_box_dataset(
    dataset: xr.Dataset, area: tuple[int, int, int, int]
) -> xr.Dataset:
    """
    Clips a box from the dataset by using a tuple. The tuple consinst
    of minx, miny, maxx and maxy values.
    """
    return dataset.clip_box(
        minx=area[0], miny=area[1], maxx=area[2], maxy=area[3], crs=dataset.crs
    )


def reduce_area(
    data: xr.Dataset, variable: str, municipality: gpd.GeoDataFrame
) -> xr.DataArray:
    """Reduces the given dataset to a two-dimensional data array by calculating
    the mean value of the specified variable within the boundaries of the
    provided municipality.
    """
    data_area = clip_dataset(data, municipality)
    data_2d = calculate_along_dimension(
        data_area[variable], ["x", "y"], xr.DataArray.mean
    )
    return data_2d
