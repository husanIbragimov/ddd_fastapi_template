from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryDTO(BaseModel):
    uuid: Optional[UUID] = None
    name: str
    description: Optional[str] = None