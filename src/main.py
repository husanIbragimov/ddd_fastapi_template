from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.handlers.auth import router as auth_router
from core.settings import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    root_path=settings.API_PREFIX,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)
app.include_router(auth_router)


@app.get("/app", response_model=dict, tags=["app"])
def main():
    return {
        "message": "FastAPI is running!",
    }
