from application.dto.auth_dto import UserRegisterDTO, UserLoginDTO, AuthTokenOutputDTO
from application.mapper.to_entity import to_entity
from core.response.exception_response import ExceptionResponse
from domain.repository.user_repository import UserRepository
from infrastructure.security.jwt_auth_service import verify_password, create_access_token


class SignUpUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserRegisterDTO) -> (AuthTokenOutputDTO, ExceptionResponse):
        dto.validate_password()
        if await self.repo.get_by_email(dto.email):
            raise ExceptionResponse(
                status_code=400,
                response_code=None,
                detail="Email is already registered."
            )

        user = to_entity(dto)

        await self.repo.save(user)
        token = create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token), None


class SignInUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserLoginDTO) -> AuthTokenOutputDTO:
        user = await self.repo.get_by_email(dto.email)

        if not user or not verify_password(dto.password, user.hashed_password):
            raise ExceptionResponse(
                status_code=401,
                response_code=None,
                detail="Invalid email or password."
            )

        token = create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)
