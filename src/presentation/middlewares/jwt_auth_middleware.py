from typing import Optional, Set

from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import decode, InvalidTokenError

from core.exceptions import BaseApplicationException
from core.response import ErrorCode
from core.settings import settings

# Public endpoints that don't require authentication
PUBLIC_ENDPOINTS: Set[str] = {
    "/auth/signin",
    "/auth/signup",
    "/docs",
    "/openapi.json",
    "/",
    "/health"
}


class AuthenticationMiddleware:

    def __init__(self, public_endpoints: Set[str] = None):
        self.public_endpoints = public_endpoints or PUBLIC_ENDPOINTS

    async def __call__(self, request: Request, call_next):
        # Skip authentication for public endpoints
        if self._is_public_endpoint(request.url.path):
            return await call_next(request)

        # Extract and validate token
        token = self._extract_token(request)
        if not token:
            return self._unauthorized_response("Token not provided")

        try:
            payload = self._validate_token(token)
            request.state.user_id = payload.get('user_id')
            request.state.user_claims = payload

            return await call_next(request)

        except InvalidTokenError as e:
            return self._unauthorized_response(f"Invalid token: {str(e)}")

    def _is_public_endpoint(self, path: str) -> bool:
        return any(path.startswith(endpoint) for endpoint in self.public_endpoints)

    @staticmethod
    def _extract_token(request: Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        return auth_header.split(" ")[1]

    def _validate_token(self, token: str) -> dict:
        return decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

    @staticmethod
    def _unauthorized_response(message: str) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error_code": ErrorCode.PERMISSION_DENIED.value,
                "message": message
            }
        )


# Initialize middleware
auth_middleware = AuthenticationMiddleware()
