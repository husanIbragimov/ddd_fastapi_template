from domain import entity
from infrastructure.persistence import models


def user_model_to_entity(user: models.UserModel) -> entity.UserEntity:
    return entity.UserEntity(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        date_joined=user.date_joined,
        hashed_password=user._hashed_password,
    )

def user_entity_to_model(user: entity.UserEntity) -> models.UserModel:
    return models.UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        _hashed_password=user.hashed_password,
        date_joined=user.date_joined,
        username=user.username,
    )
