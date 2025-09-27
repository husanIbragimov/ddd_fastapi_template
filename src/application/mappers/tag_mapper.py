from application.dto import TagDTO
from domain.entity import TagEntity


def tag_dto_to_entity(tag_dto: TagDTO) -> TagEntity:
    return TagEntity(
        uuid=tag_dto.uuid,
        name=tag_dto.name
    )


def tag_entity_to_dto(tag_entity: TagEntity) -> TagDTO:
    return TagDTO(
        uuid=tag_entity.uuid,
        name=tag_entity.name
    )
