from fastapi import HTTPException


class MunicipalityHistoricalDataNotFound(HTTPException):
    """Raise when historical municipality data is not found in the database"""

    def __init__(
        self,
        m_id: int,
        parameter: str,
        status_code: int = 404,
    ) -> None:
        self.message = (
            f"There is no historical municipality data in the "
            f"database with {m_id=} and {parameter=}"
        )
        super().__init__(status_code, self.message)


class MunicipalityHistoricalDataAlreadyExists(HTTPException):
    """Raise when historical municipality data is already found in the database"""

    def __init__(
        self,
        m_id: int,
        parameter: str,
        status_code: int = 400,
    ) -> None:
        self.message = (
            f"There is already a historical municipality data document "
            f"in the database with {m_id=} and {parameter=}"
        )
        super().__init__(status_code, self.message)
