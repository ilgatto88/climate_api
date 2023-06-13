from dataclasses import dataclass

import geopandas

from climate_data_processing import (
    config,
    geodataframe_tools,
)


@dataclass
class OeksMunicipality1DData:
    municipality_id: str
    municipality_name: str
    municipality_state: str
    scenario: str
    parameter: str
    temporal_resolution: str
    analysis_start_year: int
    analysis_end_year: int
    ensemble_start_year: int
    ensemble_end_year: int

    def create_input_file_path(self) -> str:
        return (
            f"{config.BASE_DATA_PATH}climate_data/netcdf/{self.scenario}/"
            f"oeks-{self.scenario}-{self.parameter}-austria-YS.nc"
        )

    def load_geodataframe(self) -> geopandas.GeoDataFrame:
        geo_df = geodataframe_tools.load_shapefile(config.MUNICIPALITY_SHAPEFILE)
        return geodataframe_tools.filter_geodataframe_by_ids(
            geo_df, [self.municipality_id]
        )
