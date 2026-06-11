from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Application user."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notification_settings: Mapped["NotificationSettings"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    user_settings: Mapped["UserSettings"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


class RefreshToken(UUIDMixin, TimestampMixin, Base):
    """Persisted refresh token metadata."""

    __tablename__ = "refresh_tokens"
    __table_args__ = (UniqueConstraint("jti", name="uq_refresh_tokens_jti"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    jti: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="refresh_tokens")


class NotificationSettings(UUIDMixin, TimestampMixin, Base):
    """User notification preferences."""

    __tablename__ = "notification_settings"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    follow_up_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interview_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weekly_digest: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    offer_deadline_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped[User] = relationship(back_populates="notification_settings")


class UserSettings(UUIDMixin, TimestampMixin, Base):
    """User display and goal settings."""

    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), default="Asia/Calcutta", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    weekly_goal: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    user: Mapped[User] = relationship(back_populates="user_settings")

