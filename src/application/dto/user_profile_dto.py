from typing import Optional

from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserProfileDTO(BaseModel):
    uuid: Optional[UUID] = None
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: EmailStr
    phone_number: str
