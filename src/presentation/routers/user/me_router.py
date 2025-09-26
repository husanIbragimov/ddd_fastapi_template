from fastapi import Depends, Request

from uuid import UUID

from application.dto import UserProfileDTO
from application.usecases import UserProfileUseCase
from di import container
from presentation.routers.user import user_router
from presentation.routers.user.schema import UserProfileSchema

@user_router.get("/me", response_model=UserProfileSchema, status_code=200)
async def get_user_me(
        request: Request,
        use_case: UserProfileUseCase = Depends(lambda: container.get(UserProfileUseCase))
) -> UserProfileDTO:
    user_id: UUID = request.state.user_id
    return await use_case.execute(user_id)