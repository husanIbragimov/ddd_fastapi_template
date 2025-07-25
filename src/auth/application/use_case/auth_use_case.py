from auth.application.dto.auth_dto import UserRegisterDTO, UserLoginDTO, AuthTokenOutputDTO
from auth.application.mapper.to_entity import to_entity
from auth.domain.repositories import UserRepository
from auth.infrastructure.security.jwt_auth_service import hash_password, verify_password, create_access_token


class SignUpUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserRegisterDTO) -> AuthTokenOutputDTO:
        if await self.repo.get_by_email(dto.email):
            raise ValueError("Email already registered.")

        user = to_entity(dto)

        await self.repo.save(user)
        token = create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)


class SignInUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserLoginDTO) -> AuthTokenOutputDTO:
        user = await self.repo.get_by_email(dto.email)

        if not user or not verify_password(dto.password, user.hashed_password):
            raise ValueError("Invalid credentials.")

        token = create_access_token({"sub": str(user.uuid)})
        return AuthTokenOutputDTO(access_token=token)
