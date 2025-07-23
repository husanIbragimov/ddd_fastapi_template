from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    first_name: str
    last_name: str
    passport_series: str
    passport_number: str
    phone_number: str
    email: EmailStr
    password: str
    confirmed_password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
