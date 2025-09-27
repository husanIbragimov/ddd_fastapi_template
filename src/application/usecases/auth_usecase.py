from injector import inject, singleton

from application.dto import (
    UserLoginDTO,
    UserRegisterDTO,
    AuthTokenOutputDTO,
)
from application.exceptions import ExcResponse, errors
from application.mappers import to_entity
from domain.repository import UserRepository
from domain.services.security import TokenService


@singleton
class SignUpUseCase:

    @inject
    def __init__(self, repo: UserRepository, token_service: TokenService):
        self.repo = repo
        self.token_service = token_service

    async def execute(self, dto: UserRegisterDTO) -> AuthTokenOutputDTO | ExcResponse:

        try:
            dto.validate_password()
            if await self.repo.get_by_email(dto.email):
                raise ExcResponse(
                    status_code=400,
                    error="Email is already registered."
                )

            user = to_entity(dto)

            await self.repo.save(user)
            token = self.token_service.create_access_token({"user_id": str(user.uuid)})
            return AuthTokenOutputDTO(access_token=token)
        except errors.InternalServerError as err:
            raise ExcResponse(
                status_code=500,
                error=f"Internal Server Error: {err}"
            )



@singleton
class SignInUseCase:

    @inject
    def __init__(self, repo: UserRepository, token_service: TokenService):
        self.repo = repo
        self.token_service = token_service

    async def execute(self, dto: UserLoginDTO) -> AuthTokenOutputDTO:
        user = await self.repo.get_by_email(dto.email)
        verify_pwd = self.token_service.verify_password(dto.password, user.hashed_password)
        print("USER:", user)
        print("VERIFY PWD:", verify_pwd)

        if not user or not verify_pwd:
            raise ExcResponse(
                status_code=400,
                error="Invalid email or password."
            )

        token = self.token_service.create_access_token({"user_id": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)
