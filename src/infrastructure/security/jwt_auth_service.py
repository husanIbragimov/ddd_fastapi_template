from datetime import timedelta, datetime, timezone
from typing import Dict, Any, Optional

import bcrypt
import jwt

from core.settings import settings
from domain.services.security import TokenService


class JwtToken(TokenService):
    """Simple and efficient JWT authentication service"""

    ALGORITHM = settings.JWT_ALGORITHM
    SECRET_KEY = settings.SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash a plain password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()

        # Set expiration time
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode["exp"] = expire
        to_encode["iat"] = datetime.now(timezone.utc)

        # Encode and return token
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()

        # Set expiration time
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode["exp"] = expire
        to_encode["iat"] = datetime.now(timezone.utc)

        # Encode and return token
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> Dict[str, Any]:
        """Decode and verify a JWT token"""
        return jwt.decode(
            token,
            cls.SECRET_KEY,
            algorithms=[cls.ALGORITHM]
        )

    def create_token_pair(self, payload: dict) -> dict:
        """Create a pair of access and refresh tokens"""
        access_token = self.create_access_token(payload, timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = self.create_refresh_token(payload, timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
