from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


class TokenType(StrEnum):
    """Supported JWT token types."""

    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL_VERIFY = "email_verify"
    PASSWORD_RESET = "password_reset"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def create_token(subject: str, token_type: TokenType, expires_delta: timedelta) -> tuple[str, str, datetime]:
    """Create a signed JWT and return token, jti, and expiry."""
    expires_at = datetime.now(UTC) + expires_delta
    jti = str(uuid4())
    payload = {
        "sub": subject,
        "type": token_type.value,
        "jti": jti,
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, jti, expires_at


def decode_token(token: str, expected_type: TokenType | None = None) -> dict[str, str]:
    """Decode a JWT and optionally enforce its type."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc

    token_type = payload.get("type")
    if expected_type and token_type != expected_type.value:
        raise ValueError("Invalid token type")
    if not payload.get("sub") or not payload.get("jti"):
        raise ValueError("Invalid token payload")
    return payload


def create_access_token(user_id: str) -> tuple[str, str, datetime]:
    """Create a 15-minute access token."""
    return create_token(
        user_id,
        TokenType.ACCESS,
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: str) -> tuple[str, str, datetime]:
    """Create a 7-day refresh token."""
    return create_token(
        user_id,
        TokenType.REFRESH,
        timedelta(days=settings.refresh_token_expire_days),
    )


def create_email_verification_token(user_id: str) -> str:
    """Create an email verification token."""
    token, _, _ = create_token(
        user_id,
        TokenType.EMAIL_VERIFY,
        timedelta(minutes=settings.email_verification_expire_minutes),
    )
    return token

