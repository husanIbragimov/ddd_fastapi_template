from application.dto import (
    UserLoginDTO,
    UserRegisterDTO,
    AuthTokenOutputDTO,
)
from application.exceptions import ExcResponse
from application.mappers import to_entity
from domain.repository import UserRepository
from infrastructure.security import JwtToken


class SignUpUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserRegisterDTO) -> AuthTokenOutputDTO:
        dto.validate_password()
        if await self.repo.get_by_email(dto.email):
            raise ExcResponse(
                status_code=400,
                response_code=None,
                error="Email is already registered."
            )

        user = to_entity(dto)

        await self.repo.save(user)
        token = JwtToken.create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)


class SignInUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserLoginDTO) -> AuthTokenOutputDTO:
        user = await self.repo.get_by_email(dto.email)

        if not user or not JwtToken.verify_password(dto.password, user.hashed_password):
            raise ExcResponse(
                status_code=401,
                response_code=None,
                error="Invalid email or password."
            )

        token = JwtToken.create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)
