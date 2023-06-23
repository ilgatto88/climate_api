from pydantic import BaseModel, Field


class Municipality(BaseModel):
    """Stores municpality related data."""

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
