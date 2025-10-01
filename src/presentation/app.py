from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBearer

from core.settings import settings
from infrastructure.persistence.db_session import startup_db, shutdown_db
from presentation.middlewares import auth_middleware, handle_error_middleware


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Application lifecycle manager
    - Startup: Database connection
    - Shutdown: Close database connections
    """
    # Startup
    print("🚀 Starting application...")
    await startup_db()
    print("✅ Application started successfully")

    yield  # Application is running

    # Shutdown
    print("🛑 Shutting down application...")
    await shutdown_db()
    print("✅ Application shutdown complete")

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    root_path=settings.API_PREFIX,
    dependencies=[
        Depends(HTTPBasic(auto_error=False)),
        Depends(HTTPBearer(auto_error=False))
    ]
)

app.middleware("http")(auth_middleware)
app.middleware("http")(handle_error_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


@app.on_event("startup")
async def startup():
    await startup_db()


@app.on_event("shutdown")
async def shutdown():
    await shutdown_db()
