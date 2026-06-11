from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.routers.deps import CurrentUserDep, SessionDep, bearer_scheme
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    ProfileUpdateRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenPair,
    UserRead,
    VerifyEmailRequest,
)
from app.schemas.common import ApiResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[UserRead], status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: SessionDep) -> ApiResponse[UserRead]:
    """Register a new user and send email verification."""
    user = await auth_service.register(session, payload)
    return ApiResponse(data=UserRead.model_validate(user), message="Registration successful")


@router.post("/login", response_model=ApiResponse[TokenPair])
async def login(payload: LoginRequest, response: Response, session: SessionDep, request: Request) -> ApiResponse[TokenPair]:
    """Authenticate user and return access and refresh tokens."""
    _ = request
    user = await auth_service.authenticate(session, payload.email, payload.password)
    access_token, refresh_token = await auth_service.issue_token_pair(session, user)
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=settings.refresh_token_expire_days * 86400,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
    )
    return ApiResponse(
        data=TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=UserRead.model_validate(user),
        ),
        message="Login successful",
    )


@router.post("/refresh", response_model=ApiResponse[dict[str, str | int]])
async def refresh(
    payload: RefreshRequest,
    session: SessionDep,
    refresh_token: str | None = Cookie(default=None),
) -> ApiResponse[dict[str, str | int]]:
    """Swap a refresh token for a new access token."""
    token = payload.refresh_token or refresh_token
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token is required")
    access_token = await auth_service.refresh_access_token(session, token)
    return ApiResponse(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        },
        message="Token refreshed",
    )


@router.post("/logout", response_model=ApiResponse[dict[str, bool]])
async def logout(
    session: SessionDep,
    response: Response,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    refresh_token: str | None = Cookie(default=None),
) -> ApiResponse[dict[str, bool]]:
    """Logout and blacklist active tokens."""
    if credentials:
        await auth_service.logout(session, credentials.credentials, refresh_token)
    response.delete_cookie("refresh_token")
    return ApiResponse(data={"logged_out": True}, message="Logged out")


@router.post("/forgot-password", response_model=ApiResponse[dict[str, bool]])
async def forgot_password(payload: ForgotPasswordRequest) -> ApiResponse[dict[str, bool]]:
    """Send a password reset OTP if the email exists."""
    await auth_service.start_password_reset(payload.email)
    return ApiResponse(data={"sent": True}, message="If the account exists, an OTP has been sent")


@router.post("/reset-password", response_model=ApiResponse[dict[str, bool]])
async def reset_password(payload: ResetPasswordRequest, session: SessionDep) -> ApiResponse[dict[str, bool]]:
    """Verify OTP and reset password."""
    await auth_service.reset_password(session, payload.email, payload.otp, payload.new_password)
    return ApiResponse(data={"reset": True}, message="Password reset complete")


@router.post("/verify-email", response_model=ApiResponse[UserRead])
async def verify_email(payload: VerifyEmailRequest, session: SessionDep) -> ApiResponse[UserRead]:
    """Verify an email address with a verification token."""
    user = await auth_service.verify_email(session, payload.token)
    return ApiResponse(data=UserRead.model_validate(user), message="Email verified")


@router.get("/me", response_model=ApiResponse[UserRead])
async def me(current_user: CurrentUserDep) -> ApiResponse[UserRead]:
    """Return the current user profile."""
    return ApiResponse(data=UserRead.model_validate(current_user))


@router.put("/me", response_model=ApiResponse[UserRead])
async def update_me(
    payload: ProfileUpdateRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[UserRead]:
    """Update the current user's profile."""
    user = await auth_service.update_profile(session, current_user, payload)
    return ApiResponse(data=UserRead.model_validate(user), message="Profile updated")


@router.put("/me/password", response_model=ApiResponse[dict[str, bool]])
async def change_password(
    payload: ChangePasswordRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Change the current user's password."""
    await auth_service.change_password(session, current_user, payload)
    return ApiResponse(data={"changed": True}, message="Password changed")


@router.delete("/me", response_model=ApiResponse[dict[str, bool]])
async def delete_me(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, bool]]:
    """Soft-delete the current user's account."""
    await auth_service.soft_delete(session, current_user)
    return ApiResponse(data={"deleted": True}, message="Account deleted")
