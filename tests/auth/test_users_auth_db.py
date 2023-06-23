import pytest
from pydantic import EmailStr

from src.auth import service as auth_service
from src.auth.models import UserSchema


@pytest.mark.anyio
async def test_create_user():
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    user = UserSchema(**user_data)

    await auth_service.create_user(user)
    result = await auth_service.fetch_user_by_email(user.email)
    assert result is not None
    assert result["fullname"] == "testuser"
    assert result["email"] == "test@example.com"


@pytest.mark.anyio
async def test_fetch_fetch_user_by_email():
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    user = UserSchema(**user_data)
    result = await auth_service.fetch_user_by_email(user.email)
    assert result is not None
    assert result["fullname"] == "testuser"
    assert result["email"] == "test@example.com"


@pytest.mark.anyio
async def test_remove_user():
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    user = UserSchema(**user_data)
    await auth_service.remove_user(user.email)
    result = await auth_service.fetch_user_by_email(user.email)
    assert result is None


@pytest.mark.anyio
async def test_remove_user_not_found():
    result = await auth_service.remove_user("test@example.com")
    assert result is False
