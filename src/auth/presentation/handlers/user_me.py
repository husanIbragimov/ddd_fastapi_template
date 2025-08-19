from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.use_case import SignUpUseCase, SignInUseCase
from auth.infrastructure.orm.db import get_db_session
from auth.infrastructure.orm.repository.user_repository_impl import SQLAlchemyUserRepository
from auth.presentation.handlers.schema.user_schema import UserSchema
from auth.presentation.mappers import user_signup_req_to_dto, user_signin_req_to_dto

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserSchema, status_code=200)
async def get_user_me(db: AsyncSession = Depends(get_db_session)):
    ...