from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel
from fastapi.responses import JSONResponse

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error_code: Optional[int] = None
    error_details: Optional[dict] = None

    @classmethod
    def success_response(cls, data: T = None, message: str = "Success") -> "ApiResponse[T]":
        return cls(success=True, data=data, message=message)

    @classmethod
    def error_response(
        cls,
        message: str,
        error_code: int = None,
        error_details: dict = None
    ) -> "ApiResponse[None]":
        return cls(
            success=False,
            message=message,
            error_code=error_code,
            error_details=error_details
        )

def create_success_response(data: Any = None, message: str = "Success") -> JSONResponse:
    response = ApiResponse.success_response(data=data, message=message)
    return JSONResponse(content=response.dict(), status_code=200)

def create_error_response(
    message: str,
    status_code: int = 400,
    error_code: int = None,
    error_details: dict = None
) -> JSONResponse:
    response = ApiResponse.error_response(
        message=message,
        error_code=error_code,
        error_details=error_details
    )
    return JSONResponse(content=response.dict(), status_code=status_code)