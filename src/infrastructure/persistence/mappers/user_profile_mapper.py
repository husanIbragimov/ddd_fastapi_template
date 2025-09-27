from domain import entity
from infrastructure.persistence import models


def profile_model_to_entity(user: models.UserModel) -> entity.UserProfileEntity:
    return entity.UserProfileEntity(
        uuid=user.uuid,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        date_joined=user.date_joined,
    )
