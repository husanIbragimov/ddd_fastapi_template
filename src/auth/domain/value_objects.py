from pydantic import BaseModel, EmailStr


class EmailVO(EmailStr):
    pass


class PasswordVO(BaseModel):
    raw: str

    def validate(self, value: str) -> str:
        if len(self.raw) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return self.raw
