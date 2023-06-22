import pytest
from fastapi import HTTPException, Request
from jwt.exceptions import DecodeError, ExpiredSignatureError

from app.auth.auth_bearer import JWTBearer


@pytest.fixture
def mock_jwt_bearer(mocker):
    mocker.patch(
        "app.auth.auth_bearer.decodeJWT",
        return_value={"sub": "user123"},
    )


@pytest.mark.anyio
async def test_jwt_bearer(mock_jwt_bearer, mocker):
    bearer = JWTBearer()
    request = mocker.Mock(spec=Request)
    request.headers = {"Authorization": "Bearer valid_token"}

    # Test with valid token
    credentials = await bearer(request)
    assert credentials == "valid_token"

    # Test with invalid scheme
    request.headers = {"Authorization": "InvalidScheme valid_token"}
    with pytest.raises(HTTPException):
        await bearer(request)

    # Test with invalid or expired token
    mocker.patch(
        "app.auth.auth_bearer.decodeJWT",
        side_effect=DecodeError,
    )
    request.headers = {"Authorization": "Bearer invalid_token"}
    with pytest.raises(HTTPException):
        await bearer(request)

    mocker.patch(
        "app.auth.auth_bearer.decodeJWT",
        side_effect=ExpiredSignatureError,
    )
    request.headers = {"Authorization": "Bearer expired_token"}
    with pytest.raises(HTTPException):
        await bearer(request)

    # Test without authorization code
    request.headers = {}
    with pytest.raises(HTTPException):
        await bearer(request)
