import time

import jwt
from decouple import UndefinedValueError, config
from jwt.exceptions import DecodeError

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

if not isinstance(JWT_ALGORITHM, str) or not isinstance(JWT_SECRET, str):
    raise UndefinedValueError(
        "Please set the secret key and algorithm value in your .env file!"
    )


def signJWT(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}


def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return (
            decoded_token
            if decoded_token["expires"] >= time.time()
            else None  # type: ignore
        )
    except DecodeError:
        return None
