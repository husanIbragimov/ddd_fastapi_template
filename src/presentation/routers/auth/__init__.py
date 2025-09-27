from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

from .login_router import *
from .register_router import *