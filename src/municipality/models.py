from typing import Optional

from pydantic import BaseModel, Field


class Municipality(BaseModel):
    """Stores municipality related data."""

    m_id: int = Field(gt=0, description="Municipality ID", lt=100000)
    name: str = Field(min_length=1, max_length=50, description="Municipality name")
    state: str = Field(min_length=1, max_length=50, description="Municipality state")

    class Config:
        schema_extra = {
            "example": {
                "m_id": 99999,
                "name": "Testcity",
                "state": "Teststate",
            }
        }


class MunicipalityUpdate(BaseModel):
    """Stores municipality related data for update."""

    name: Optional[str] = None
    state: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Testcity",
                "state": "Teststate",
            }
        }
