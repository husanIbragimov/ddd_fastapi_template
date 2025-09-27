from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=["user"])

from .me_router import *
