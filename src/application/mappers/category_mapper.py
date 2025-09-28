from application.dto.category_dto import CategoryDTO
from domain.entity.category_entity import CategoryEntity


def cat_to_entity(dto: CategoryDTO) -> CategoryEntity:
    return CategoryEntity(
        uuid=None,
        name=dto.name,
        description=dto.description
    )

def cat_to_dto(entity: CategoryEntity) -> CategoryDTO:
    return CategoryDTO(
        uuid=entity.uuid,
        name=entity.name,
        description=entity.description
    )
