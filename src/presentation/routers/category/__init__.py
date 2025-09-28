from fastapi import APIRouter

category_router = APIRouter(prefix="/category", tags=["category"])

from .category_post_router import *
from .category_detail_router import *
from .category_list_router import *
