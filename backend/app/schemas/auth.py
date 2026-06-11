from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRead(BaseModel):
    """Public user profile."""

    id: str
    email: EmailStr
    name: str
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class RegisterRequest(BaseModel):
    """Registration payload."""

    email: EmailStr
    name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenPair(BaseModel):
    """Access and refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead


class RefreshRequest(BaseModel):
    """Refresh payload."""

    refresh_token: str | None = None


class ForgotPasswordRequest(BaseModel):
    """Forgot password payload."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Password reset payload."""

    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8, max_length=128)


class VerifyEmailRequest(BaseModel):
    """Email verification payload."""

    token: str


class ProfileUpdateRequest(BaseModel):
    """Profile update payload."""

    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None


class ChangePasswordRequest(BaseModel):
    """Change password payload."""

    current_password: str
    new_password: str = Field(min_length=8, max_length=128)

