from application.dto.category_dto import CategoryDTO
from domain.repository.category_repository import CategoryRepository
from application.mapper.to_entity import cat_to_entity

class CategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, data: CategoryDTO):
        cat_entity = cat_to_entity(data)
        return self.category_repository.create(cat_entity)

    def get_category(self, category_id):
        return self.category_repository.get_by_pk(category_id)