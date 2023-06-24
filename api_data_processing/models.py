from dataclasses import dataclass

import geopandas

from api_data_processing import config, geodataframe_tools
from api_data_processing.static_geo import VIENNA_GIDS


@dataclass
class MunicipalityDataSettings:
    """Stores settings for 1 dimensional climate data."""

    municipalityId: int
    climateParameter: str
    temporal_resolution: str
    analysis_start_year: int
    analysis_end_year: int
    ensemble_start_year: int
    ensemble_end_year: int

    def create_future_input_file_path(self, scenario: str) -> str:
        """Creates the future input file path string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/{scenario}/"
            f"oeks-{scenario}-{self.climateParameter}-austria-YS.nc"
        )

    def create_historical_input_file_path(self) -> str:
        """Creates the historical input file string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/historical/"
            f"spartacus-{self.climateParameter}-austria-YS.nc"
        )

    def load_geodataframe(self) -> geopandas.GeoDataFrame:
        """Loads the geodataframe for the chosen municipality."""
        geo_df = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
        if self.municipalityId == 90000:
            id_list = VIENNA_GIDS
        else:
            id_list = [str(self.municipalityId)]
        return geodataframe_tools.filter_geodataframe_by_ids(geo_df, id_list)
