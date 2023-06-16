import asyncio

import bcrypt
from pydantic import EmailStr

from core.database import admin
from core.models import UserSchema

user_collection = admin.User


async def fetch_user_by_email(email: str) -> dict[str, str] | None:
    """
    Retrieves a user from the collection based on the email address.
    """
    document = await user_collection.find_one({"email": email})
    return document


async def create_user(user: UserSchema) -> UserSchema:
    """
    Inserts a new user document into the collection
    and returns the created user.
    """

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user.password = hashed_password.decode()

    await user_collection.insert_one(user.dict())
    return user


async def remove_user(email: str) -> bool:
    """
    Deletes an user document from the collection based
    on the given email address, and returns True if the deletion was successful.
    """
    user_exists = await user_collection.find_one({"email": user.email})
    if user_exists:
        await user_collection.delete_one({"email": email})
        return True
    return False


async def delete_all_users() -> None:
    """Removes all municipalities from the database"""
    x = await user_collection.delete_many({})
    print(f"Removed all ({x.deleted_count}) users from the database.")


if __name__ == "__main__":
    user = UserSchema(
        fullname="Joe",
        email=EmailStr("jt@example.com"),
        password="hello123",
    )

    loop = asyncio.new_event_loop()
    try:
        # print(loop.run_until_complete(create_user(user)))
        print(loop.run_until_complete(fetch_user_by_email(user.email)))
        # print(loop.run_until_complete(remove_user(user.email)))
        # loop.run_until_complete(delete_all_users())
    except KeyboardInterrupt:
        pass
