import os
import time

import jwt
from decouple import UndefinedValueError, config
from dotenv import load_dotenv
from jwt.exceptions import DecodeError


def get_jwt_variables() -> tuple[str, str]:
    if not os.path.isfile(".env"):
        load_dotenv(".env-example")

    JWT_SECRET = config("JWT_SECRET", cast=str)
    JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)

    if not isinstance(JWT_ALGORITHM, str) or not isinstance(JWT_SECRET, str):
        raise UndefinedValueError(
            "Please set the secret key and algorithm value in your .env file!"
        )
    return (JWT_SECRET, JWT_ALGORITHM)


def signJWT(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    jwt_secret, jwt_algorithm = get_jwt_variables()
    token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)

    return {"access_token": token}


def decodeJWT(token: str) -> dict | None:
    jwt_secret, jwt_algorithm = get_jwt_variables()
    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return (
            decoded_token
            if decoded_token["expires"] >= time.time()
            else None  # type: ignore
        )
    except DecodeError:
        return None
