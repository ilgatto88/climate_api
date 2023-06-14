from dataclasses import dataclass

import geopandas

from climate_data_processing import config, geodataframe_tools
from core.api_models import Municipality


@dataclass
class MunicipalityDataSettings:
    """Stores settings for 1 dimensional climate data."""

    municipality: Municipality
    scenario: str
    parameter: str
    temporal_resolution: str
    analysis_start_year: int
    analysis_end_year: int
    ensemble_start_year: int
    ensemble_end_year: int

    def create_future_input_file_path(self) -> str:
        """Creates the future input file path string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/{self.scenario}/"
            f"oeks-{self.scenario}-{self.parameter}-austria-YS.nc"
        )

    def create_historical_input_file_path(self) -> str:
        """Creates the historical input file string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/historical/"
            f"spartacus-{self.parameter}-austria-YS.nc"
        )

    def load_geodataframe(self) -> geopandas.GeoDataFrame:
        """Loads the geodataframe for the chosen municipality."""
        geo_df = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
        return geodataframe_tools.filter_geodataframe_by_ids(
            geo_df, [str(self.municipality.m_id)]
        )
