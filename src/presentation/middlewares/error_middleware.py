from typing import Callable, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from core.exceptions import (
    BaseApplicationException,
    ValidationException,
    EntityNotFoundException,
    InfrastructureException
)
from core.response import ApiResponse, ErrorCode
from utils.logger import logger


class GlobalExceptionHandler:
    """Centralized exception handler for all application errors"""

    @staticmethod
    async def __call__(request: Request, call_next: Callable) -> JSONResponse:
        try:
            response = await call_next(request)
            return response

        except RequestValidationError as exc:
            return GlobalExceptionHandler._handle_validation_error(exc, request)

        except ValidationException as exc:
            return GlobalExceptionHandler._handle_custom_validation_error(exc, request)

        except EntityNotFoundException as exc:
            return GlobalExceptionHandler._handle_not_found_error(exc, request)

        except InfrastructureException as exc:
            return GlobalExceptionHandler._handle_infrastructure_error(exc, request)

        except BaseApplicationException as exc:
            return GlobalExceptionHandler._handle_application_error(exc, request)

        except IntegrityError as exc:
            return GlobalExceptionHandler._handle_integrity_error(exc, request)

        except SQLAlchemyError as exc:
            return GlobalExceptionHandler._handle_database_error(exc, request)

        except HTTPException as exc:
            return GlobalExceptionHandler._handle_http_exception(exc, request)

        except StarletteHTTPException as exc:
            return GlobalExceptionHandler._handle_starlette_exception(exc, request)

        except Exception as exc:
            return GlobalExceptionHandler._handle_unexpected_error(exc, request)

    @staticmethod
    def _handle_validation_error(exc: RequestValidationError, request: Request) -> JSONResponse:
        """Handle FastAPI validation errors"""
        logger.warning(
            "validation_error",
            path=str(request.url),
            errors=exc.errors(),
            body=exc.body
        )

        # Format validation errors
        formatted_errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            formatted_errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"]
            })

        response = ApiResponse.error_response(
            message="Validation error occurred",
            error_code=ErrorCode.VALIDATION_ERROR.value,
            error_details={
                "validation_errors": formatted_errors,
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_custom_validation_error(exc: ValidationException, request: Request) -> JSONResponse:
        """Handle custom validation exceptions"""
        logger.warning(
            "custom_validation_error",
            path=str(request.url),
            field=exc.details.get("field"),
            message=exc.message
        )

        response = ApiResponse.error_response(
            message=exc.message,
            error_code=exc.error_code.value,
            error_details={
                **exc.details,
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_not_found_error(exc: EntityNotFoundException, request: Request) -> JSONResponse:
        """Handle entity not found errors"""
        logger.info(
            "entity_not_found",
            path=str(request.url),
            entity=exc.details.get("entity_name"),
            entity_id=exc.details.get("entity_id")
        )

        response = ApiResponse.error_response(
            message=exc.message,
            error_code=exc.error_code.value,
            error_details={
                **exc.details,
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_infrastructure_error(exc: InfrastructureException, request: Request) -> JSONResponse:
        """Handle infrastructure layer errors"""
        logger.error(
            "infrastructure_error",
            path=str(request.url),
            message=exc.message,
            error_code=exc.error_code.name,
            cause=str(exc.cause) if exc.cause else None
        )

        response = ApiResponse.error_response(
            message="A system error occurred. Please try again later.",
            error_code=exc.error_code.value,
            error_details={
                "path": str(request.url),
                "timestamp": str(request.state.__dict__.get("request_time"))
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_application_error(exc: BaseApplicationException, request: Request) -> JSONResponse:
        """Handle application layer errors"""
        logger.error(
            "application_error",
            path=str(request.url),
            message=exc.message,
            error_code=exc.error_code.name,
            details=exc.details
        )

        # Map error codes to HTTP status codes
        status_mapping = {
            ErrorCode.VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
            ErrorCode.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
            ErrorCode.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.BUSINESS_RULE_VIOLATION: status.HTTP_409_CONFLICT,
            ErrorCode.DUPLICATE_ENTITY_ERROR: status.HTTP_409_CONFLICT,
        }

        http_status = status_mapping.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = ApiResponse.error_response(
            message=exc.message,
            error_code=exc.error_code.value,
            error_details={
                **exc.details,
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=http_status,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_integrity_error(exc: IntegrityError, request: Request) -> JSONResponse:
        """Handle database integrity constraint violations"""
        logger.error(
            "integrity_error",
            path=str(request.url),
            error=str(exc.orig)
        )

        # Parse constraint violation
        error_msg = str(exc.orig)
        if "duplicate key" in error_msg.lower() or "unique constraint" in error_msg.lower():
            message = "A record with this data already exists"
            error_code = ErrorCode.DUPLICATE_ENTITY_ERROR
        elif "foreign key" in error_msg.lower():
            message = "Referenced resource does not exist"
            error_code = ErrorCode.BUSINESS_RULE_VIOLATION
        else:
            message = "Database constraint violation"
            error_code = ErrorCode.DATABASE_ERROR

        response = ApiResponse.error_response(
            message=message,
            error_code=error_code.value,
            error_details={
                "path": str(request.url),
                "constraint": "database_constraint"
            }
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_database_error(exc: SQLAlchemyError, request: Request) -> JSONResponse:
        """Handle general database errors"""
        logger.error(
            "database_error",
            path=str(request.url),
            error=str(exc)
        )

        response = ApiResponse.error_response(
            message="A database error occurred. Please try again later.",
            error_code=ErrorCode.DATABASE_ERROR.value,
            error_details={
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_http_exception(exc: HTTPException, request: Request) -> JSONResponse:
        """Handle FastAPI HTTP exceptions"""
        logger.warning(
            "http_exception",
            path=str(request.url),
            status_code=exc.status_code,
            detail=exc.detail
        )

        response = ApiResponse.error_response(
            message=str(exc.detail),
            error_code=exc.status_code,
            error_details={
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_starlette_exception(exc: StarletteHTTPException, request: Request) -> JSONResponse:
        """Handle Starlette HTTP exceptions"""
        logger.warning(
            "starlette_exception",
            path=str(request.url),
            status_code=exc.status_code,
            detail=exc.detail
        )

        response = ApiResponse.error_response(
            message=str(exc.detail),
            error_code=exc.status_code,
            error_details={
                "path": str(request.url)
            }
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump()
        )

    @staticmethod
    def _handle_unexpected_error(exc: Exception, request: Request) -> JSONResponse:
        """Handle unexpected errors"""
        logger.critical(
            "unexpected_error",
            path=str(request.url),
            error_type=type(exc).__name__,
            error=str(exc),
            exc_info=True
        )

        response = ApiResponse.error_response(
            message="An unexpected error occurred. Please contact support.",
            error_code=ErrorCode.DATABASE_ERROR.value,
            error_details={
                "path": str(request.url),
                "error_type": type(exc).__name__
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )


# Middleware instance
handle_error_middleware = GlobalExceptionHandler()