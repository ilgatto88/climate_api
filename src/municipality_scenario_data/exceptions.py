from fastapi import HTTPException


class MunicipalityScenarioDataNotFound(HTTPException):
    """Raise when municipality scenario data is not found in the database"""

    def __init__(
        self,
        m_id: int,
        parameter: str,
        scenario: str,
        status_code: int = 404,
    ) -> None:
        self.message = (
            f"There is no municipality scenario data in the "
            f"database with {m_id=}, {parameter=} and {scenario=}"
        )
        super().__init__(status_code, self.message)


class MunicipalityScenarioDataAlreadyExists(HTTPException):
    """Raise when municipality scenario data is already found in the database"""

    def __init__(
        self,
        m_id: int,
        parameter: str,
        scenario: str,
        status_code: int = 400,
    ) -> None:
        self.message = (
            f"There is already a municipality scenario data document "
            f"in the database with {m_id=}, {parameter=} and {scenario=}"
        )
        super().__init__(status_code, self.message)
