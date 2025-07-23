from uuid import uuid4

from .dto.auth_dto import UserRegisterDTO, UserLoginDTO, AuthTokenOutputDTO
from ..domain.entities import UserEntity
from ..domain.repositories import UserRepository
from ..infrastructure.security.jwt_auth_service import hash_password, verify_password, create_access_token


class SignUpUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, dto: UserRegisterDTO) -> AuthTokenOutputDTO:
        if await self.repo.get_by_email(dto.email):
            raise ValueError("Email already registered.")

        hashed_pw = hash_password(dto.validate_password())
        user = UserEntity(
            uuid=uuid4(),
            first_name=dto.first_name,
            last_name=dto.last_name,
            passport_series=dto.passport_series,
            passport_number=dto.passport_number,
            phone_number=dto.phone_number,
            email=str(dto.email),
            hashed_password=hashed_pw,
            date_joined=dto.date_joined
        )

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
