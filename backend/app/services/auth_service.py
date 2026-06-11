from datetime import UTC, datetime, timedelta
from secrets import randbelow

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.redis import blacklist_jti, is_jti_blacklisted, redis_client
from app.core.security import (
    TokenType,
    create_access_token,
    create_email_verification_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.base import utc_now
from app.models.user import NotificationSettings, RefreshToken, User, UserSettings
from app.schemas.auth import ChangePasswordRequest, ProfileUpdateRequest, RegisterRequest
from app.services.email_service import email_service


class AuthService:
    """Business logic for authentication and account management."""

    async def register(self, session: AsyncSession, payload: RegisterRequest) -> User:
        """Create a user and send an email verification token."""
        existing = await session.scalar(select(User).where(User.email == payload.email.lower()))
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

        user = User(
            email=payload.email.lower(),
            name=payload.name,
            hashed_password=hash_password(payload.password),
        )
        user.notification_settings = NotificationSettings()
        user.user_settings = UserSettings()
        session.add(user)
        await session.commit()
        await session.refresh(user)

        token = create_email_verification_token(user.id)
        await email_service.send_verification_email(user.email, token)
        return user

    async def authenticate(self, session: AsyncSession, email: str, password: str) -> User:
        """Validate credentials with account lockout."""
        user = await session.scalar(select(User).where(User.email == email.lower(), User.is_deleted.is_(False)))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        now = utc_now()
        locked_until = user.locked_until
        if locked_until and locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=UTC)
        if locked_until and locked_until > now:
            raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Account temporarily locked")

        if not verify_password(password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= settings.login_lockout_failures:
                user.locked_until = now + timedelta(minutes=settings.login_lockout_minutes)
            await session.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        user.failed_login_attempts = 0
        user.locked_until = None
        await session.commit()
        return user

    async def issue_token_pair(self, session: AsyncSession, user: User) -> tuple[str, str]:
        """Create access and refresh tokens and persist refresh metadata."""
        access_token, _, _ = create_access_token(user.id)
        refresh_token, refresh_jti, refresh_expires_at = create_refresh_token(user.id)
        session.add(RefreshToken(user_id=user.id, jti=refresh_jti, expires_at=refresh_expires_at))
        await session.commit()
        return access_token, refresh_token

    async def refresh_access_token(self, session: AsyncSession, refresh_token: str) -> str:
        """Exchange a valid refresh token for a new access token."""
        payload = decode_token(refresh_token, TokenType.REFRESH)
        if await is_jti_blacklisted(str(payload["jti"])):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        token_record = await session.scalar(
            select(RefreshToken).where(
                RefreshToken.jti == payload["jti"],
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > datetime.now(UTC),
            )
        )
        if not token_record:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        access_token, _, _ = create_access_token(str(payload["sub"]))
        return access_token

    async def logout(self, session: AsyncSession, access_token: str, refresh_token: str | None) -> None:
        """Blacklist active tokens."""
        payload = decode_token(access_token, TokenType.ACCESS)
        exp_seconds = max(1, int(payload["exp"]) - int(datetime.now(UTC).timestamp()))
        await blacklist_jti(str(payload["jti"]), exp_seconds)

        if refresh_token:
            refresh_payload = decode_token(refresh_token, TokenType.REFRESH)
            await redis_client.setex(f"blacklist:{refresh_payload['jti']}", settings.refresh_token_expire_days * 86400, "1")
            token_record = await session.scalar(select(RefreshToken).where(RefreshToken.jti == refresh_payload["jti"]))
            if token_record:
                token_record.revoked_at = utc_now()
                await session.commit()

    async def start_password_reset(self, email: str) -> None:
        """Create and store a short-lived OTP for password reset."""
        otp = f"{randbelow(1_000_000):06d}"
        await redis_client.setex(f"password_reset:{email.lower()}:{otp}", settings.reset_otp_expire_minutes * 60, "1")
        await email_service.send_password_reset_otp(email.lower(), otp)

    async def reset_password(self, session: AsyncSession, email: str, otp: str, new_password: str) -> None:
        """Verify a password reset OTP and update the password."""
        if not await redis_client.get(f"password_reset:{email.lower()}:{otp}"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

        user = await session.scalar(select(User).where(User.email == email.lower(), User.is_deleted.is_(False)))
        if not user:
            return
        user.hashed_password = hash_password(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None
        await redis_client.delete(f"password_reset:{email.lower()}:{otp}")
        await session.commit()

    async def verify_email(self, session: AsyncSession, token: str) -> User:
        """Verify a user's email address."""
        payload = decode_token(token, TokenType.EMAIL_VERIFY)
        user = await self.get_user(session, str(payload["sub"]))
        user.is_verified = True
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user(self, session: AsyncSession, user_id: str) -> User:
        """Fetch a non-deleted user."""
        user = await session.scalar(select(User).where(User.id == user_id, User.is_deleted.is_(False)))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_profile(self, session: AsyncSession, user: User, payload: ProfileUpdateRequest) -> User:
        """Update user profile fields."""
        if payload.email and payload.email.lower() != user.email:
            existing = await session.scalar(select(User).where(User.email == payload.email.lower()))
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
            user.email = payload.email.lower()
            user.is_verified = False
        if payload.name:
            user.name = payload.name
        await session.commit()
        await session.refresh(user)
        return user

    async def change_password(self, session: AsyncSession, user: User, payload: ChangePasswordRequest) -> None:
        """Change a user's password after verifying the current password."""
        if not verify_password(payload.current_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        user.hashed_password = hash_password(payload.new_password)
        await session.commit()

    async def soft_delete(self, session: AsyncSession, user: User) -> None:
        """Soft-delete a user account."""
        user.is_deleted = True
        user.deleted_at = utc_now()
        await session.commit()


auth_service = AuthService()
