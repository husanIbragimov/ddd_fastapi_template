import uuid
from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from typing import Dict, Any
from typing import Optional

import bcrypt
import jwt
from passlib.context import CryptContext

from core.settings import settings
from domain.services.security import TokenService
from infrastructure.errors import errors
from utils.timezone import utcnow


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class JwtToken(TokenService):
    ALGORITHM = settings.JWT_ALGORITHM
    SIGNING_KEY = settings.SECRET_KEY
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
    REFRESH_TOKEN_EXPIRE = timedelta(days=7)

    def create_token_pair(self, payload: dict) -> TokenPair:
        access = self.create_access_token(payload, self.ACCESS_TOKEN_EXPIRE)
        refresh = self.create_refresh_token(payload, self.REFRESH_TOKEN_EXPIRE)
        return TokenPair(access_token=access, refresh_token=refresh)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except errors.VerificationError:
            return False

    @classmethod
    def hash_password(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')


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
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + cls.ACCESS_TOKEN_EXPIRE
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SIGNING_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + cls.REFRESH_TOKEN_EXPIRE
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SIGNING_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
