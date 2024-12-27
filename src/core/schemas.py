from typing import Annotated

from pydantic import BaseModel, Field


class Health(BaseModel):
    version: Annotated[str, Field(..., json_schema_extra={"example": "0.0.1"})]
    status: Annotated[str, Field(..., json_schema_extra={"example": "Healthy"})]
    database: Annotated[str, Field(..., json_schema_extra={"example": "Unhealthy"})]
