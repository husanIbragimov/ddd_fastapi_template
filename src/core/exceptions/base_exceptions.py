from typing import Optional, Dict, Any
from core.response import ErrorCode


class BaseApplicationException(Exception):
    """Base exception for all application errors"""

    def __init__(
            self,
            message: str,
            error_code: ErrorCode,
            details: Optional[Dict[str, Any]] = None,
            cause: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        super().__init__(message)


class DomainException(BaseApplicationException):
    """Domain layer exceptions"""
    pass


class ApplicationException(BaseApplicationException):
    """Application layer exceptions"""
    pass


class InfrastructureException(BaseApplicationException):
    """Infrastructure layer exceptions"""
    pass


# Specific exceptions
class EntityNotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            f"{entity_name} with id {entity_id} not found",
            ErrorCode.RESOURCE_NOT_FOUND,
            {"entity_name": entity_name, "entity_id": entity_id}
        )


class ValidationException(DomainException):
    def __init__(self, field: str, message: str):
        super().__init__(
            f"Validation error in field '{field}': {message}",
            ErrorCode.VALIDATION_ERROR,
            {"field": field, "validation_message": message}
        )
