from injector import inject, singleton

from application.dto import (
    UserLoginDTO,
    UserRegisterDTO,
    AuthTokenOutputDTO,
)
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

    async def execute(self, dto: UserRegisterDTO) -> ApiResponse[dict[str, str]] | None:
        try:
            # Validate input data
            self._validate_registration_data(dto)

            # Check if the user already exists
            existing_email = await self.repo.get_by_email(dto.email)
            if existing_email:
                raise ValidationException(
                    "email", "Email already in use",
                )

            # Save the user to the repository
            if user_id := await self.repo.save(self._create_user_entity(dto)):
                return ApiResponse.success_response(
                    data={"user_id": str(user_id)},
                    message="User registered successfully",
                )
        except ValidationException as e:
            raise
        except Exception as e:
            raise ApplicationException(
                f"Failed to register user: {e}",
                ErrorCode.DATABASE_ERROR,
                cause=e
            )

    @staticmethod
    def _validate_registration_data(dto: UserRegisterDTO) -> ApiResponse | None:
        if dto.hashed_password != dto.confirmed_password:
            return ApiResponse.error_response(
                message="Passwords do not match",
                error_code=400,
            )

        if len(dto.hashed_password) < 8:
            return ApiResponse.error_response(
                message="Password must be at least 8 characters long",
                error_code=400,
            )
        return None

    def _create_user_entity(self, dto: UserRegisterDTO) -> UserEntity:
        hashed_pwd = self.token_service.hash_password(dto.hashed_password)

        return to_entity(dto, hashed_pwd)


@singleton
class SignInUseCase:

    @inject
    def __init__(self, repo: UserRepository, token_service: TokenService):
        self.repo = repo
        self.token_service = token_service

    async def execute(self, dto: UserLoginDTO) -> ApiResponse[AuthTokenOutputDTO | None]:
        try:
            # Get user by email
            user = await self.repo.get_by_email(dto.email)
            print(user)
            if not self._validate_user(user, dto.password):
                return ApiResponse.error_response(
                    message="Invalid email or password",
                    error_code=401
                )

            # Generate JWT access token
            token = self.token_service.create_token_pair({"user_id": str(user.uuid)})
            return ApiResponse.success_response(
                data=AuthTokenOutputDTO(
                    access_token=token.get("access_token"),
                    refresh_token=token.get("refresh_token")
                ),
                message="User logged in successfully"
            )
        except ApplicationException as e:
            return ApiResponse.error_response(
                message=e.message,
                error_code=401
            )
        except Exception as e:
            return ApiResponse.error_response(
                message="Authentication failed",
                error_code=500,
                error_details={"error": str(e)}
            )

    def _validate_user(self, user: UserEntity, password: str) -> bool:
        if not user:
            return False
        return self.token_service.verify_password(password, user.hashed_password)
