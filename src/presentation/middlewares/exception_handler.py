from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core.response import ApiResponse


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log the exception (you can replace with proper logger)
            print(f"Unhandled exception: {e}")

            # Use our unified error response
            return create_error_response(
                message=str(e),
                status_code=500,
                error_code=1000,  # You can map your own error codes
                error_details={"path": str(request.url)}
            )


def create_success_response(data: Any = None, message: str = "Success") -> JSONResponse:
    response = ApiResponse.success_response(data=data, message=message)
    return JSONResponse(content=response.dict(), status_code=200)


def create_error_response(
        message: str,
        status_code: int = 400,
        error_code: Optional[int] = None,
        error_details: Optional[dict] = None
) -> JSONResponse:
    response = ApiResponse.error_response(
        message=message,
        error_code=error_code,
        error_details=error_details
    )
    return JSONResponse(content=response.dict(), status_code=status_code)

handle_error_middleware = ExceptionHandlingMiddleware