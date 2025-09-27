from uuid import UUID

from injector import inject, singleton
from pydantic.v1 import EmailStr

from application.exceptions import errors
from domain.repository import UserRepository
from domain.services.security import TokenService


@singleton
class UserAuthTokenService:
    @inject
    def __init__(self, token_service: TokenService, user_repo: UserRepository):
        self.token_service = token_service
        self.user_repo = user_repo

    async def generate_token_for_user(self, user_id: UUID) -> str | errors.InternalServerError:
        user = await self.user_repo.get_by_uuid(user_id)
        if not user:
            raise errors.InternalServerError
        payload = {"user_id": str(user.uuid)}
        return self.token_service.create_access_token(payload)

    async def validate_user_credentials(self, email: str, password: str) -> bool | errors.InternalServerError:
        user = await self.user_repo.get_by_email(EmailStr(email))
        if not user:
            return errors.InternalServerError("User not found")
        return self.token_service.verify_password(password, user.hashed_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.token_service.verify_password(plain_password, hashed_password)

    def create_access_token(self, payload: dict) -> str:
        return self.token_service.create_access_token(payload)
