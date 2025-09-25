from pydantic import BaseModel
from typing import Optional

class CategoryDTO(BaseModel):
    name: str
    description: Optional[str] = None