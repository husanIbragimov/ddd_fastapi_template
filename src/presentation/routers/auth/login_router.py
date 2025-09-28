from fastapi import Depends

from core.response import ApiResponse

from application.usecases import SignInUseCase
from di import container
from presentation.mappers import signin_req_to_dto
from presentation.routers.auth import auth_router
from presentation.routers.auth.schema import SignInRequest


@auth_router.post("/signin", response_model=ApiResponse)
async def signin(
        data: SignInRequest,
        use_case: SignInUseCase = Depends(
            lambda: container.get(SignInUseCase)
        )
):
    to_dto = signin_req_to_dto(data)
    result = await use_case.execute(to_dto)
    return result
