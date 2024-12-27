from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, UUID4


class BaseSchema(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: datetime
    updated_at: datetime
