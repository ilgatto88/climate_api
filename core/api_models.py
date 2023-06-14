from pydantic import BaseModel


class Municipality(BaseModel):
    """Stores municpality related data."""

    m_id: int
    name: str
    state: str
