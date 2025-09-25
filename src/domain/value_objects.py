from pydantic import BaseModel, EmailStr

from core.response.exception_response import ExceptionResponse


class EmailVO(EmailStr):
    pass


class PasswordVO(BaseModel):
    raw: str

    def validate(self, value: str) -> str:
        if len(self.raw) < 6:
            raise ExceptionResponse(
                status_code=400,
                response_code=None,
                detail="Password must be at least 6 characters long."
            )
        return self.raw
