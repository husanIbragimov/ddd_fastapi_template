import uuid

from application.dto.auth_dto import UserRegisterDTO
from domain.entity.user_entity import UserEntity


def to_entity(dto: UserRegisterDTO, hashed_pw: str) -> UserEntity:
    return UserEntity(
        uuid=uuid.uuid4(),
        first_name=dto.first_name,
        last_name=dto.last_name,
        phone_number=dto.phone_number,
        email=str(dto.email),
        date_joined=dto.date_joined,
        username=dto.username,
        hashed_password=hashed_pw
    )

