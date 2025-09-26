from fastapi import Depends

from application.usecases import SignUpUseCase
from di import container
from presentation.mappers import signup_req_to_dto
from presentation.routers.auth import auth_router
from presentation.routers.auth.schema.auth_schema import SignUpRequest, AuthTokenResponse


@auth_router.post("/signup", response_model=AuthTokenResponse, status_code=201)
async def signup(
        data: SignUpRequest,
        use_case: SignUpUseCase = Depends(
            lambda: container.get(SignUpUseCase)
        )
) -> AuthTokenResponse:
    to_dto = signup_req_to_dto(data)
    result = await use_case.execute(to_dto)
    return AuthTokenResponse(**result.dict())
