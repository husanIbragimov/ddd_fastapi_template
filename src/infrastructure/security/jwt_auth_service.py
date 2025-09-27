import uuid
from datetime import timedelta, datetime, timezone
from typing import Dict, Any
from typing import Optional

import jwt
from passlib.context import CryptContext

from core.settings import settings
from domain.services.security import TokenService
from utils.timezone import utcnow


class JwtToken(TokenService):
    ALGORITHM = settings.JWT_ALGORITHM
    SIGNING_KEY = settings.SECRET_KEY
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, raw: str | None, hashed: str | None) -> bool:
        return cls.pwd_context.verify(raw, hashed)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def encode(cls, payload: Dict[str, Any], expired=timedelta(minutes=10)) -> str:
        payload["exp"]: datetime = (utcnow() + expired).timestamp()
        payload["iat"]: float = utcnow().now().timestamp()
        payload['jti']: str = str(uuid.uuid4())

        return jwt.encode(payload, cls.SIGNING_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode(cls, token: str, verify: bool = True) -> Dict[str, Any] | None:
        return jwt.decode(
            token, cls.SIGNING_KEY, algorithms=[cls.ALGORITHM],
            options={"verify_signature": verify}
        )

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SIGNING_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
