from domain.entity.category_entity import CategoryEntity
from infrastructure.persistence.models.category_model import CategoryModel


def category_entity_to_model(category_entity: CategoryEntity) -> CategoryModel:
    return CategoryModel(
        name=category_entity.name,
        description=category_entity.description
    )
