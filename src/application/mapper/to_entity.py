import uuid

from application.dto.auth_dto import UserRegisterDTO
from domain.entity.user_entity import UserEntity
from infrastructure.security.jwt_auth_service import hash_password


def to_entity(dto: UserRegisterDTO) -> UserEntity:
    hashed_pw = hash_password(dto.hashed_password)

    return UserEntity(
        uuid=uuid.uuid4(),
        first_name=dto.first_name,
        last_name=dto.last_name,
        passport_series=dto.passport_series,
        passport_number=dto.passport_number,
        phone_number=dto.phone_number,
        email=str(dto.email),
        hashed_password=hashed_pw,
        date_joined=dto.date_joined
    )
