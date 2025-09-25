from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.orm.db import get_db_session
from presentation.handlers.schema.user_schema import UserSchema

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserSchema, status_code=200)
async def get_user_me(db: AsyncSession = Depends(get_db_session)):
    ...