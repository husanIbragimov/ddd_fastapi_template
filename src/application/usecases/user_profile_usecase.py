from uuid import UUID

from injector import inject, singleton

from application.dto import UserProfileDTO
from application.mappers import profile_entity_to_dto
from core.exceptions import EntityNotFoundException
from core.response import ApiResponse
from domain.repository import UserProfileRepository


@singleton
class UserProfileUseCase:

    @inject
    def __init__(self, repo: UserProfileRepository):
        self.repo = repo

    async def execute(self, pk: UUID) -> ApiResponse[UserProfileDTO | None]:
        if user := await self.repo.get_by_uuid(pk):
            user_mapper = profile_entity_to_dto(user)
            return ApiResponse.success_response(
                data=user_mapper,
                message="User profile found successfully"
            )

        raise EntityNotFoundException(
            entity_name="User",
            entity_id=str(pk)
        )
