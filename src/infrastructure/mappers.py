from .orm.models import UserModel
from domain.entity.user_entity import UserEntity


def user_model_to_entity(user: UserModel) -> UserEntity:
    return UserEntity(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        passport_series=user.passport_series,
        passport_number=user.passport_number,
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
        passport_series=user.passport_series,
        passport_number=user.passport_number,
        phone_number=user.phone_number,
        email=user.email,
        _hashed_password=user.hashed_password,
        date_joined=user.date_joined,
    )
