from fastapi import HTTPException


class MunicipalityDataNotFound(HTTPException):
    """Raise when municipality data is not found in the database"""

    def __init__(
        self,
        m_id: int,
        status_code: int = 404,
    ) -> None:
        self.message = f"There is no municipality data in the database with {m_id=}"
        super().__init__(status_code, self.message)


class MunicipalityDataAlreadyExists(HTTPException):
    """Raise when municipality data is already found in the database"""

    def __init__(
        self,
        m_id: int,
        status_code: int = 400,
    ) -> None:
        self.message = (
            f"There is already a municipality data document "
            f"in the database with {m_id=}"
        )
        super().__init__(status_code, self.message)
