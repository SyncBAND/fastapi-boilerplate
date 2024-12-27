import re

from typing import Annotated, ClassVar

from pydantic import (
    BaseModel, ConfigDict, EmailStr, Field, StringConstraints, UUID4, field_validator, model_validator
)

from src.app.users.schemas import UserSchema


class CurrentUserSchema(BaseModel):
    id: Annotated[UUID4, Field(None)]
    is_authenticated: Annotated[bool, Field(False)]

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


# pylint: disable=no-self-argument
class RegisterUserSchema(UserSchema):
    password: Annotated[str, StringConstraints(min_length=8, max_length=16)]
    confirm_password: Annotated[str, StringConstraints(min_length=8, max_length=16)]

    @field_validator("password")
    def password_must_contain_special_characters(cls, value) -> str:
        if not re.search(r"[^a-zA-Z0-9]", value):
            raise ValueError("Password must contain special characters")
        return value

    @field_validator("password")
    def password_must_contain_numbers(cls, value) -> str:
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain numbers")
        return value

    @field_validator("password")
    def password_must_contain_uppercase(cls, value) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain uppercase characters")
        return value

    @field_validator("password")
    def password_must_contain_lowercase(cls, value) -> str:
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain lowercase characters")
        return value

    @model_validator(mode='after')
    def passwords_match(self) -> 'RegisterUserSchema':
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
