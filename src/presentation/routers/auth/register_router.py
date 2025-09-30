from fastapi import Depends

from application.usecases import SignUpUseCase
from core.response import ApiResponse
from di import container
from presentation.mappers import signup_req_to_dto
from presentation.routers.auth import auth_router
from presentation.routers.auth.schema.auth_schema import SignUpRequest


@auth_router.post("/signup", response_model=ApiResponse)
async def signup(
        data: SignUpRequest,
        use_case: SignUpUseCase = Depends(
            lambda: container.get(SignUpUseCase)
        )
):
    try:
        to_dto = signup_req_to_dto(data)
        result = await use_case.execute(to_dto)
        print(result)
        return result
    except Exception as e:
        return ApiResponse.error_response(
            message="Registration failed",
            error_code=400,
            error_details={"error": str(e)}
        )
