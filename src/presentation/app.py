from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBearer

from core.settings import settings
from presentation.middlewares import json_renderer_middleware, jwt_auth_middleware, validation_error_middleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

app.middleware("http")(validation_error_middleware)
app.middleware("http")(json_renderer_middleware)
app.middleware("http")(jwt_auth_middleware)
