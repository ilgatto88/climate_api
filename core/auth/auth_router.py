import bcrypt
from fastapi import APIRouter, Body, HTTPException

from core.app.models import UserLoginSchema, UserSchema
from core.auth import auth_db
from core.auth.auth_handler import signJWT

router = APIRouter()


@router.post("/signup", include_in_schema=False)
async def create_user(user: UserSchema = Body(...)) -> dict[str, str]:
    """
    Creates a new user in the database with the provided data
    and returns the JWT token.
    """
    user_exists = await auth_db.fetch_user_by_email(user.email)

    if user_exists:
        raise HTTPException(
            status_code=400,
            detail=f"User with email '{user.email}' already exists.",
        )

    response = await auth_db.create_user(user)
    if response:
        return signJWT(user.email)
    raise HTTPException(status_code=400, detail="Bad Request")


@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)) -> dict[str, str]:
    """
    User gets logged in and a JWT token gets returned if the user exists,
    otherwise a message is returned.
    """
    if await check_user(user):
        return signJWT(user.email)
    raise HTTPException(401, "Email or password incorrect!")


async def check_user(user: UserLoginSchema) -> bool:
    """Checks if the user already exists in the database."""
    response_user: dict[str, str] | None = await auth_db.fetch_user_by_email(user.email)

    if response_user:
        hashed_password = response_user.get("password")
        entered_password = user.password.encode()
        if hashed_password is not None:
            password_valid = bcrypt.checkpw(entered_password, hashed_password.encode())
            if password_valid:
                return True
    return False
