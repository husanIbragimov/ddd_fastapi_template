from datetime import datetime
from typing import Union, Optional
from uuid import UUID

from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    uuid: UUID
    first_name: str
    last_name: Optional[str]
    username: str
    phone_number: str
    email: str
    date_joined: Union[datetime, str]
