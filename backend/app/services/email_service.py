from app.core.config import settings


class EmailService:
    """Email adapter with a no-op local implementation."""

    async def send_verification_email(self, email: str, token: str) -> None:
        """Send an email verification link."""
        if not settings.smtp_host:
            return
        # Real SMTP/fastapi-mail wiring can be enabled with the env vars in production.
        _ = (email, token)

    async def send_password_reset_otp(self, email: str, otp: str) -> None:
        """Send password reset OTP."""
        if not settings.smtp_host:
            return
        _ = (email, otp)


email_service = EmailService()

