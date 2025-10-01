from typing import Optional
from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError

from infrastructure.security.jwt_auth_service import JwtToken


class AuthenticationMiddleware:
    """Simple JWT authentication middleware for FastAPI"""

    # Public endpoints that don't require authentication
    PUBLIC_PATHS = {
        "/auth/",       # All auth endpoints (signin, signup, etc.)
        "/docs",        # Swagger docs
        "/openapi.json",
        "/redoc",
        "/health",      # Health check
        "/favicon.ico"
    }

    async def __call__(self, request: Request, call_next):
        """Process request and validate JWT token if required"""

        # Skip authentication for public endpoints
        if self._is_public_path(request.url.path):
            return await call_next(request)

        # Extract token from Authorization header
        token = self._extract_bearer_token(request)
        if not token:
            return self._error_response("Missing authentication token", 401)

        try:
            # Decode and verify JWT token
            payload = JwtToken.decode_token(token)

            # Extract user_id and set it in request state
            user_id_str = payload.get("user_id")
            if not user_id_str:
                return self._error_response("Invalid token: missing user_id", 401)

            # Convert user_id to UUID and store in request state
            request.state.user_id = UUID(user_id_str)
            request.state.token_payload = payload

            return await call_next(request)

        except InvalidTokenError as e:
            return self._error_response(f"Invalid or expired token: {str(e)}", 401)
        except ValueError:
            return self._error_response("Invalid user_id format in token", 401)
        except Exception as e:
            return self._error_response(f"Authentication error: {str(e)}", 401)

    def _is_public_path(self, path: str) -> bool:
        """Check if the path is public (doesn't require authentication)"""
        # Remove API prefix if exists
        clean_path = path.replace("/api/v1", "")
        return any(clean_path.startswith(public) for public in self.PUBLIC_PATHS)

    @staticmethod
    def _extract_bearer_token(request: Request) -> Optional[str]:
        """Extract Bearer token from Authorization header"""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header.split(" ", 1)[1]
        return None

    @staticmethod
    def _error_response(message: str, status_code: int) -> JSONResponse:
        """Return standardized error response"""
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "error_code": status_code
            }
        )


# Initialize middleware instance
auth_middleware = AuthenticationMiddleware()
