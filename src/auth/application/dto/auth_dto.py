from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegisterDTO(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    passport_series: str
    passport_number: str
    phone_number: str
    email: EmailStr
    hashed_password: str
    confirmed_password: str
    date_joined: datetime = Field(default_factory=datetime.utcnow)

    def validate_password(self):
        if self.hashed_password != self.confirmed_password:
            raise ValueError("Passwords do not match")
        if len(self.hashed_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return self.hashed_password


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


class AuthTokenOutputDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
