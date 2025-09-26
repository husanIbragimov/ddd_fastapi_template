from pydantic.v1 import EmailStr

from application.dto.user_profile_dto import UserProfileDTO
from domain.entity import UserProfileEntity


def profile_entity_to_dto(user: UserProfileEntity) -> UserProfileDTO:
    return UserProfileDTO(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=EmailStr(user.email),
        phone_number=user.phone_number,
    )
