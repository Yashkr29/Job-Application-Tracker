from app.models.application import ApplicationStatus


TERMINAL_STATUSES = {
    ApplicationStatus.OFFER.value,
    ApplicationStatus.REJECTED.value,
    ApplicationStatus.WITHDRAWN.value,
    ApplicationStatus.GHOSTED.value,
}


def is_terminal_status(status: str) -> bool:
    """Return whether a status ends the active pipeline."""
    return status in TERMINAL_STATUSES

