from typing import Optional, Union
from datetime import datetime

from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserProfileDTO(BaseModel):
    uuid: UUID
    first_name: str
    last_name: Optional[str] = None
    username: str
    email: str
    phone_number: str
    date_joined: Union[datetime, str] = None
