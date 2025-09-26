from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserProfileEntity:
    uuid: UUID | None
    first_name: str
    last_name: str | None
    username: str
    email: str
    phone_number: str
    date_joined: datetime | None = None