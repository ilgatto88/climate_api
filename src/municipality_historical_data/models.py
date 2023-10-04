from pydantic import BaseModel, Field


class MunicipalityHistoricalData(BaseModel):
    """Helper class for MunicipalityHistoricalData"""

    municipalityId: int = Field(gt=0, lt=100000)
    source: str = Field(min_length=1, max_length=100)
    climateParameter: str = Field(min_length=1, max_length=50)
    temporalResolution: str = Field(min_length=1, max_length=50)
    analysisTimeRange: list[int] = Field(min_items=1, max_items=150)
    rawData: list[float] = Field(min_items=1, max_items=150)
    statistics0D: dict[str, dict[str, float]]
