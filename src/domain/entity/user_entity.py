from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserEntity:
    uuid: UUID
    first_name: str
    last_name: str | None
    username: str
    phone_number: str
    email: str
    date_joined: datetime
    hashed_password: str | None = None
