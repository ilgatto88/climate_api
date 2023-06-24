from fastapi import HTTPException


class MunicipalityNotFound(HTTPException):
    """Raise when municipality is not found in the database"""

    def __init__(
        self,
        m_id: int,
        status_code: int = 404,
    ) -> None:
        self.message = f"There is no municipality in the database with {m_id=}"
        super().__init__(status_code, self.message)


class MunicipalityAlreadyExists(HTTPException):
    """Raise when municipality is already found in the database"""

    def __init__(
        self,
        m_id: int,
        status_code: int = 400,
    ) -> None:
        self.message = f"There is already a municipality in the database with {m_id=}"
        super().__init__(status_code, self.message)
