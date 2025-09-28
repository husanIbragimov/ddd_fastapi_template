from typing import Optional, Generic, TypeVar, Any

from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Any
    error_code: Optional[int] = None
    error_details: Optional[dict] = None

    @classmethod
    def success_response(cls, data: T = None, message: str = "Success") -> "ApiResponse[T]":
        return cls(
            success=True,
            data=data,
            message=message
        )

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
