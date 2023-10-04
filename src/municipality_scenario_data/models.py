from typing import Optional

from pydantic import BaseModel, Field


class Statistics1D(BaseModel):
    """Helper class for MunicipalityDataScenario"""

    minimum: list[float] = Field(min_items=1, max_items=150)
    lowerPercentile: list[float] = Field(min_items=1, max_items=150)
    median: list[float] = Field(min_items=1, max_items=150)
    mean: list[float] = Field(min_items=1, max_items=150)
    upperPercentile: list[float] = Field(min_items=1, max_items=150)
    maximum: list[float] = Field(min_items=1, max_items=150)


class MunicipalityScenarioData(BaseModel):
    """Helper class for MunicipalityDataScenario"""

    municipalityId: int = Field(gt=0, lt=100000)
    source: str = Field(min_length=1, max_length=100)
    climateParameter: str = Field(min_length=1, max_length=50)
    temporalResolution: str = Field(min_length=1, max_length=50)
    modelNames: list[str] = Field(min_items=1, max_items=20)
    rawData: dict[str, list[Optional[float]]]
    statistics1D: Statistics1D
    statistics0D: dict[str, dict[str, float]]
