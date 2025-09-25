from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.use_case import SignUpUseCase, SignInUseCase
from infrastructure.persistence.db import get_db_session
from infrastructure.persistence.repository.user_repository_impl import SQLAlchemyUserRepository
from presentation.handlers.schema.auth_schema import SignUpRequest, SignInRequest, AuthTokenResponse
from presentation.mappers import user_signup_req_to_dto, user_signin_req_to_dto

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", response_model=AuthTokenResponse, status_code=201)
async def signup(req: SignUpRequest, db: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyUserRepository(db)
    use_case = SignUpUseCase(repo)
    token = await use_case.execute(user_signup_req_to_dto(req))
    return token


@auth_router.post("/signin", response_model=AuthTokenResponse, status_code=201)
async def signin(req: SignInRequest, db: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyUserRepository(db)
    use_case = SignInUseCase(repo)
    token = await use_case.execute(user_signin_req_to_dto(req))
    return token
