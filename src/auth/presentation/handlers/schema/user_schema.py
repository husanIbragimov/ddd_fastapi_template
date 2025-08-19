from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    passport_series: str
    passport_number: str
    phone_number: str
    email: str
    date_joined: str