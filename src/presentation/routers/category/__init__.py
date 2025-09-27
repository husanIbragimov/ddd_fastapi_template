from fastapi import APIRouter

category_router = APIRouter(prefix="/category", tags=["category"])

from .category_post_router import *