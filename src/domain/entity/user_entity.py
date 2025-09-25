from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserEntity:
    uuid: UUID
    first_name: str
    last_name: str
    passport_series: str
    passport_number: str
    phone_number: str
    email: str
    hashed_password: str
    date_joined: datetime
