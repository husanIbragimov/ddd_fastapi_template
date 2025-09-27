from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError


class InfraError(Exception):
    """Base class for database-related errors."""
    pass


class RecordNotFoundError(InfraError):
    """Raised when a database record is not found."""
    pass


class DuplicateRecordError(InfraError):
    """Raised when attempting to create a duplicate record."""
    pass


class TransactionError(InfraError):
    """Raised when a database transaction fails."""
    pass


class UnknownDatabaseError(InfraError):
    """Raised for unknown database errors."""
    pass


class VerificationError(InfraError):
    """Raised when verification of data fails."""
    pass


def handle_db_exception(exc: SQLAlchemyError) -> None:
    if isinstance(exc, NoResultFound):
        raise RecordNotFoundError("The requested record was not found.") from exc
    elif isinstance(exc, IntegrityError):
        raise DuplicateRecordError("A duplicate record exists.") from exc
    else:
        raise UnknownDatabaseError("An unknown database error occurred.") from exc

# Example usage:
# try:
#     # database operation
# except SQLAlchemyError as e:
#     handle_db_exception(e)
