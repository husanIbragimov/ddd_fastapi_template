from uuid import UUID

from injector import inject, singleton

from application.dto import TagDTO, PagingDTO
from application.exceptions import ExcResponse, errors
from application.mappers import tag_dto_to_entity, tag_entity_to_dto
from domain.repository import TagRepository


@singleton
class TagUseCase:

    @inject
    def __init__(self, repository: TagRepository):
        self.repository = repository

    async def create(self, dto: TagDTO) -> UUID | ExcResponse:
        try:
            rag_entity = tag_dto_to_entity(dto)
            result = await self.repository.create(rag_entity)
            return result
        except errors.InternalServerError as err:
            return ExcResponse(status_code=500, error=f"Internal Server Error: {err}")

    async def get_by_id(self, tag_id: UUID) -> TagDTO | ExcResponse:
        result = await self.repository.get_by_id(tag_id)
        if result is None:
            return ExcResponse(status_code=404, error="Tag not found")
        return tag_entity_to_dto(result)

    async def list(self, skip: int = 0, limit: int = 10) -> PagingDTO[TagDTO]:
        result = await self.repository.list(skip=skip, limit=limit)
        return PagingDTO[TagDTO](
            page=result.page,
            size=result.size,
            total=result.total,
            items=[tag_entity_to_dto(item) for item in result.items]
        )

    async def update(self, tag_id: UUID, dto: TagDTO) -> UUID | ExcResponse:
        try:
            tag_entity = tag_dto_to_entity(dto)
            result = await self.repository.update(tag_id, tag_entity)
            return result
        except errors.InternalServerError as err:
            return ExcResponse(status_code=500, error=f"Internal Server Error: {err}")
