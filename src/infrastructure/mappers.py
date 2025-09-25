from .persistence.models import UserModel
from domain.entity.user_entity import UserEntity


def user_model_to_entity(user: UserModel) -> UserEntity:
    return UserEntity(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        hashed_password=user.hashed_password,
        date_joined=user.date_joined,
    )


def user_entity_to_model(user: UserEntity) -> UserModel:
    return UserModel(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        _hashed_password=user.hashed_password,
        date_joined=user.date_joined,
        username=user.username,
    )
