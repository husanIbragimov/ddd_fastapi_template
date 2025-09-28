import enum
from enum import unique


@unique
class ResponseCode(enum.Enum):
    ...



class ErrorCode(enum.Enum):
    # Business Logic Errors (4000-4999)
    VALIDATION_ERROR = 4000
    UNAUTHORIZED = 4001
    BUSINESS_RULE_VIOLATION = 4002
    RESOURCE_NOT_FOUND = 4004
    PERMISSION_DENIED = 4003

    # Technical Errors (5000-5999)
    DATABASE_ERROR = 5001
    EXTERNAL_SERVICE_ERROR = 5002
    CONFIGURATION_ERROR = 5003
    DUPLICATE_ENTITY_ERROR = 5004
