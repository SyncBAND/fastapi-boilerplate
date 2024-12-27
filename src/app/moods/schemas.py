from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, UUID4

from src.core.database.schemas import BaseSchema


class MoodSchema(BaseModel):
    learning: Annotated[str, StringConstraints(min_length=10, max_length=500)]
    personal_note: Annotated[str, StringConstraints(min_length=10, max_length=500)]
    rating: Annotated[int, Field(..., json_schema_extra={"ge": 0, "le": 10})]


class MoodDetailSchema(BaseSchema, MoodSchema):
    user_id: UUID4
