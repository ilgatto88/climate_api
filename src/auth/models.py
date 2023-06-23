from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@example.com",
                "password": "any",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {"example": {"email": "joe@example.com", "password": "any"}}
