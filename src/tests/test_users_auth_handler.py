import time
from unittest.mock import ANY, patch

from jwt import DecodeError

from src.auth.auth_handler import decodeJWT, signJWT


def test_signJWT():
    user_id = "12345"
    fake_jwt_secret = "fake_secret"
    fake_jwt_algorithm = "HS256"
    fake_token = "fake_token"

    with patch("src.auth.auth_handler.get_jwt_variables") as mock_get_jwt_variables:
        mock_get_jwt_variables.return_value = (fake_jwt_secret, fake_jwt_algorithm)

        with patch("jwt.encode") as mock_jwt_encode:
            mock_jwt_encode.return_value = fake_token

            result = signJWT(user_id)

            assert result == {"access_token": fake_token}

            mock_get_jwt_variables.assert_called_once()

            mock_jwt_encode.assert_called_once_with(
                {"user_id": user_id, "expires": ANY},
                fake_jwt_secret,
                algorithm=fake_jwt_algorithm,
            )


def test_decodeJWT():
    fake_token = "fake_token"
    fake_jwt_secret = "fake_secret"
    fake_jwt_algorithm = "HS256"
    fake_decoded_token = {"user_id": "12345", "expires": time.time() + 600}

    with patch("src.auth.auth_handler.get_jwt_variables") as mock_get_jwt_variables:
        mock_get_jwt_variables.return_value = (fake_jwt_secret, fake_jwt_algorithm)

        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = fake_decoded_token

            result = decodeJWT(fake_token)
            assert result == fake_decoded_token

            mock_get_jwt_variables.assert_called_once()
            mock_jwt_decode.assert_called_once_with(
                fake_token, fake_jwt_secret, algorithms=[fake_jwt_algorithm]
            )


def test_decodeJWT_exception():
    fake_token = "fake_token"
    fake_jwt_secret = "fake_secret"
    fake_jwt_algorithm = "HS256"

    with patch("src.auth.auth_handler.get_jwt_variables") as mock_get_jwt_variables:
        mock_get_jwt_variables.return_value = (fake_jwt_secret, fake_jwt_algorithm)

        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.side_effect = DecodeError("Invalid token")

            result = decodeJWT(fake_token)

            assert result is None

            mock_get_jwt_variables.assert_called_once()

            mock_jwt_decode.assert_called_once_with(
                fake_token, fake_jwt_secret, algorithms=[fake_jwt_algorithm]
            )
