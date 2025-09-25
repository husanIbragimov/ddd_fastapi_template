from presentation.app import app
from presentation.handlers.auth import router as auth_router

app.include_router(auth_router)
