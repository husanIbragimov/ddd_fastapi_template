from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.use_cases import SignUpUseCase, SignInUseCase
from auth.infrastructure.orm.db import get_db_session
from auth.infrastructure.orm.repository.user_repository_impl import SQLAlchemyUserRepository
from auth.presentation.handlers.schema.request_models import SignUpRequest, SignInRequest, AuthTokenResponse
from auth.presentation.mappers import user_signup_req_to_dto, user_signin_req_to_dto

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthTokenResponse, status_code=201)
async def signup(req: SignUpRequest, db: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyUserRepository(db)
    use_case = SignUpUseCase(repo)
    token = await use_case.execute(user_signup_req_to_dto(req))
    return token


@router.post("/signin", response_model=AuthTokenResponse, status_code=201)
async def signin(req: SignInRequest, db: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyUserRepository(db)
    use_case = SignInUseCase(repo)
    token = await use_case.execute(user_signin_req_to_dto(req))
    return token
