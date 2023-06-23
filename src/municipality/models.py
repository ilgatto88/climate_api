from pydantic import BaseModel


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
