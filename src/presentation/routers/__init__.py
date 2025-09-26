from .auth import auth_router
from .user import user_router
from .category import category_router

routers = [
    auth_router,
    user_router,
    category_router,
]