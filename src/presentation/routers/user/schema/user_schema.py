from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserProfileSchema(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    username: EmailStr
    phone_number: str
    email: str
    date_joined: str