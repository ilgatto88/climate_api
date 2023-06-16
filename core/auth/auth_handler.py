import time

import jwt
from decouple import UndefinedValueError, config
from jwt.exceptions import DecodeError

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

if not isinstance(JWT_ALGORITHM, str) or not isinstance(JWT_SECRET, str):
    raise UndefinedValueError(
        "Please set the secret key and algorithm value in your .env file!"
    )


def token_response(token: str):
    return {"access_token": token}


def signJWT(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return (
            decoded_token
            if decoded_token["expires"] >= time.time()
            else None  # type: ignore
        )
    except DecodeError:
        return {"message": "Error, token couldn't be decoded!"}
