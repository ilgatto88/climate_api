from typing import Optional

from pydantic import BaseModel, Field


class MunicipalityDataMeta(BaseModel):
    """Helper class for MunicipalityData"""

    municipalityId: int = Field(gt=0, lt=100000)
    climateParameter: str = Field(min_length=1, max_length=50)
    temporalResolution: str = Field(min_length=1, max_length=50)
    analysisTimeRange: list[int] = Field(min_items=1, max_items=150)
    ensembleTimeRange: list[int] = Field(min_items=1, max_items=150)


class MunicipalityDataHistorical(BaseModel):
    """Helper class for MunicipalityData"""

    analysisModel: str = Field(min_length=1, max_length=100)
    rawData: list[float] = Field(min_items=1, max_items=150)
    statistics0D: dict[str, dict[str, float]]


class Statistics1D(BaseModel):
    """Helper class for MunicipalityDataRCP"""

    minimum: list[float] = Field(min_items=1, max_items=150)
    lowerPercentile: list[float] = Field(min_items=1, max_items=150)
    median: list[float] = Field(min_items=1, max_items=150)
    mean: list[float] = Field(min_items=1, max_items=150)
    upperPercentile: list[float] = Field(min_items=1, max_items=150)
    maximum: list[float] = Field(min_items=1, max_items=150)


class MunicipalityDataRCP(BaseModel):
    """Helper class for MunicipalityDataEnsemble"""

    modelNames: list[str] = Field(min_items=1, max_items=20)
    rawData: dict[str, list[Optional[float]]]
    statistics1D: Statistics1D
    statistics0D: dict[str, dict[str, float]]


class MunicipalityDataEnsemble(BaseModel):
    """Helper class for MunicipalityData"""

    rcp26: MunicipalityDataRCP
    rcp85: MunicipalityDataRCP


class MunicipalityData(BaseModel):
    """A very complex class with many nested dictionaries."""

    meta: MunicipalityDataMeta
    historical: MunicipalityDataHistorical
    ensemble: MunicipalityDataEnsemble
    ensemble: MunicipalityDataEnsemble
    ensemble: MunicipalityDataEnsemble
