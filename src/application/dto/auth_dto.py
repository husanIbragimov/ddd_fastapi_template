from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from core.exceptions import ValidationException


class UserRegisterDTO(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    phone_number: str
    username: str
    email: EmailStr
    hashed_password: str
    confirmed_password: str
    date_joined: datetime = Field(default_factory=datetime.utcnow)

    def validate_password(self) -> None:
        if self.hashed_password != self.confirmed_password:
            raise ValidationException("password", "Passwords do not match")
        if len(self.hashed_password) < 8:
            raise ValidationException("password", "Password must be at least 8 characters")


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


class AuthTokenOutputDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
