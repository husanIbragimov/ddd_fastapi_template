from typing import Optional
from uuid import UUID

from injector import inject, singleton

from application.dto import UserProfileDTO
from application.exceptions import ExcResponse
from application.mappers import profile_entity_to_dto
from domain.repository import UserProfileRepository


@singleton
class UserProfileUseCase:

    @inject
    def __init__(self, repo: UserProfileRepository):
        self.repo = repo

    async def execute(self, pk: UUID) -> Optional[UserProfileDTO]:
        if user := await self.repo.get_by_uuid(pk):
            user_mapper = profile_entity_to_dto(user)
            return user_mapper

        raise ExcResponse(
            status_code=404,
            error="User not found"
        )
