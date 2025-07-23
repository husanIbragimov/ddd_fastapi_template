from auth.application.dto.auth_dto import UserRegisterDTO, UserLoginDTO
from auth.presentation.handlers.schema.request_models import SignUpRequest, SignInRequest


def user_signup_req_to_dto(user_req: SignUpRequest) -> UserRegisterDTO:
    return UserRegisterDTO(
        first_name=user_req.first_name,
        last_name=user_req.last_name,
        passport_series=user_req.passport_series,
        passport_number=user_req.passport_number,
        phone_number=user_req.phone_number,
        email=user_req.email,
        hashed_password=user_req.password,
        confirmed_password=user_req.confirmed_password
    )


def user_signin_req_to_dto(user_req: SignInRequest) -> UserLoginDTO:
    return UserLoginDTO(
        email=user_req.email,
        password=user_req.password
    )
