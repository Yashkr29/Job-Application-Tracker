from apscheduler.schedulers.asyncio import AsyncIOScheduler


def build_scheduler() -> AsyncIOScheduler:
    """Build the application scheduler with reminder job slots."""
    scheduler = AsyncIOScheduler(timezone="Asia/Calcutta")
    return scheduler

