from uuid import UUID

from fastapi import Depends, Request

from application.dto import UserProfileDTO
from application.exceptions import ExcResponse
from application.usecases import UserProfileUseCase
from di import container
from presentation.routers.user import user_router
from presentation.routers.user.schema import UserProfileSchema


@user_router.get("/me", response_model=UserProfileSchema, status_code=200)
async def get_user_me(
        request: Request,
        use_case: UserProfileUseCase = Depends(lambda: container.get(UserProfileUseCase))
) -> UserProfileSchema:
    user_id: UUID = request.state.user_id
    if not user_id:
        raise ExcResponse(
            status_code=400,
            error="User ID not found in request state"
        )

    result = await use_case.execute(user_id)
    return UserProfileSchema(**result.dict())