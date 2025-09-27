from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TagDTO(BaseModel):
    uuid: Optional[UUID] = None
    name: dict[str, str]
