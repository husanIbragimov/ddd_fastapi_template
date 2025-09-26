from typing import Optional, Dict, Any

from fastapi import Request, HTTPException
from jwt import exceptions
from starlette.responses import JSONResponse

from infrastructure.security.jwt_auth_service import JwtToken


async def jwt_auth_middleware(request: Request, call_next) -> JSONResponse:
    request.state.user_id = None
    authorization: Optional[str] = request.headers.get("Authorization")

    if authorization and authorization.startswith("Bearer "):
        token = get_token(authorization)

        try:
            payload: Optional[Dict[str, Any]] = JwtToken.decode(token)
            if not payload or payload.get('user_id') is None:
                raise exceptions.InvalidSubjectError("Invalid token. user_id must be provided")

            request.state.user_id = payload.get('user_id')

        except exceptions.InvalidTokenError as e:
            return JSONResponse(
                status_code=401,
                content={
                    'is_success': False,
                    'status': 401,
                    'error': str(e),
                }
            )

    return await call_next(request)


def get_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    auth_header = authorization.split(" ")

    if len(auth_header) != 2:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    return auth_header[1]
