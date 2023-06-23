from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(
        min_length=1, max_length=50, strip_whitespace=False, to_lower=False
    )
    email: EmailStr
    password: str = Field(min_length=2, max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@example.com",
                "password": "any",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=2, max_length=100)

    class Config:
        schema_extra = {"example": {"email": "joe@example.com", "password": "any"}}
