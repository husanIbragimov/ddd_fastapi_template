from application.dto.category_dto import CategoryDTO
from domain.entity.category_entity import CategoryEntity


def cat_to_entity(dto: CategoryDTO) -> CategoryEntity:
    return CategoryEntity(
        uuid=dto.uuid,
        name=dto.name,
        description=dto.description
    )
