from uuid import UUID

from fastapi import Depends, Request

from application.usecases import UserProfileUseCase
from core.response import ApiResponse
from di import container
from presentation.routers.user import user_router
from presentation.routers.user.schema import UserProfileSchema


@user_router.get("/me", response_model=UserProfileSchema, status_code=200)
async def get_user_me(
        request: Request,
        use_case: UserProfileUseCase = Depends(lambda: container.get(UserProfileUseCase))
):
    if not hasattr(request.state, "user_id"):
        raise ApiResponse.error_response(
            message="User ID not found in request state",
            error_code=401
        )
    user_id: UUID = request.state.user_id

    result = await use_case.execute(user_id)
    return result
