from typing import Optional

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    uuid: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: str
