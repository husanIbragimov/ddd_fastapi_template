from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryDTO(BaseModel):
    uuid: UUID | None
    name: dict[str, str]
    description: Optional[dict[str, str]] = None