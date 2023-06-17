from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@example.com",
                "password": "any",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {"example": {"email": "joe@example.com", "password": "any"}}


class Municipality(BaseModel):
    """Stores municpality related data."""

    m_id: int
    name: str
    state: str

    class Config:
        schema_extra = {
            "example": {
                "m_id": 99999,
                "name": "Testcity",
                "state": "Teststate",
            }
        }


class MunicipalityDataMeta(BaseModel):
    """Helper class for MunicipalityData"""

    municipalityId: int
    climateParameter: str
    temporalResolution: str
    analysisTimeRange: list[int]
    ensembleTimeRange: list[int]


class MunicipalityDataHistorical(BaseModel):
    """Helper class for MunicipalityData"""

    analysisModel: str
    rawData: list[float]
    statistics0D: dict[str, dict[str, float]]


class Statistics1D(BaseModel):
    """Helper class for MunicipalityDataRCP"""

    minimum: list[float]
    lowerPercentile: list[float]
    median: list[float]
    mean: list[float]
    upperPercentile: list[float]
    maximum: list[float]


class MunicipalityDataRCP(BaseModel):
    """Helper class for MunicipalityDataEnsemble"""

    modelNames: list[str]
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
