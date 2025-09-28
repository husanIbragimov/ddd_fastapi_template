from injector import inject, singleton

from application.dto import (
    UserLoginDTO,
    UserRegisterDTO,
    AuthTokenOutputDTO,
)
from application.exceptions import ExcResponse
from application.mappers import to_entity
from core.exceptions import ValidationException, ApplicationException
from core.response import ApiResponse, ErrorCode
from domain.entity import UserEntity
from domain.repository import UserRepository
from domain.services.security import TokenService


@singleton
class SignUpUseCase:

    @inject
    def __init__(self, repo: UserRepository, token_service: TokenService):
        self.repo = repo
        self.token_service = token_service

    async def execute(self, dto: UserRegisterDTO) -> ApiResponse[AuthTokenOutputDTO]:
        try:
            # Validate input data
            self._validate_registration_data(dto)

            # Check if the user already exists
            existing_email = await self.repo.get_by_email(dto.email)
            if existing_email:
                raise ValidationException("email", "Email is already registered.")

            # Create user entity
            user_entity = self._create_user_entity(dto)

            # Save the user to the repository
            created_user = await self.repo.save(user_entity)

            # Generate token
            token = self.token_service.create_access_token({
                "user_id": str(created_user)
            })
            return ApiResponse.success_response(
                data=AuthTokenOutputDTO(access_token=token),
                message="User registered successfully"
            )
        except ValidationException as e:
            raise
        except Exception as e:
            raise ApplicationException(
                "Failed to register user",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    @staticmethod
    def _validate_registration_data(dto: UserRegisterDTO) -> None:
        if dto.hashed_password != dto.confirmed_password:
            raise ValidationException("password", "Passwords do not match.")

        if len(dto.hashed_password) < 8:
            raise ValidationException("password", "Password must be at least 8 characters long")

    def _create_user_entity(self, dto: UserRegisterDTO) -> UserEntity:
        hashed_pwd = self.token_service.hash_password(dto.hashed_password)

        return to_entity(dto, hashed_pwd)


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
