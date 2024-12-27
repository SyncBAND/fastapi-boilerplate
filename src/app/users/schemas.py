from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

from src.app.moods.schemas import MoodDetailSchema
from src.core.database.schemas import BaseSchema


class UserSchema(BaseModel):
    email: EmailStr
    firstname: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern="^[a-zA-Z]+$")]
    lastname: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern="^[a-zA-Z]+$")]


class UserDetailSchema(BaseSchema, UserSchema):
    moods: list[MoodDetailSchema]
