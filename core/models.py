import geopandas
from pydantic import BaseModel

from climate_data_processing import (
    config,
    geodataframe_tools,
)


class Municipality(BaseModel):
    """Stores municpality related data."""

    m_id: int
    name: str
    state: str


class MunicipalityData(BaseModel):
    """Stores settings for 1 dimensional climate data."""

    municipality: Municipality
    scenario: str
    parameter: str
    temporal_resolution: str
    analysis_start_year: int
    analysis_end_year: int
    ensemble_start_year: int
    ensemble_end_year: int

    def create_input_file_path(self) -> str:
        """Creates the input file path string."""
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/{self.scenario}/"
            f"oeks-{self.scenario}-{self.parameter}-austria-YS.nc"
        )

    def load_geodataframe(self) -> geopandas.GeoDataFrame:
        """Loads the geodataframe for the chosen municipality."""
        geo_df = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
        return geodataframe_tools.filter_geodataframe_by_ids(
            geo_df, [str(self.municipality.m_id)]
        )
