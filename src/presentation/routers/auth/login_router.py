from fastapi import Depends

from application.usecases import SignInUseCase
from di import container
from presentation.mappers import signin_req_to_dto
from presentation.routers.auth import auth_router
from presentation.routers.auth.schema import SignInRequest, AuthTokenResponse


@auth_router.post("/signin", response_model=AuthTokenResponse, status_code=201)
async def signin(
        data: SignInRequest,
        use_case: SignInUseCase = Depends(
            lambda: container.get(SignInUseCase)
        )
) -> AuthTokenResponse:
    to_dto = signin_req_to_dto(data)
    result = await use_case.execute(to_dto)
    return AuthTokenResponse(**result.dict())
