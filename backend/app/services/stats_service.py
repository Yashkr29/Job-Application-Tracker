from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import ApplicationStatus, JobApplication
from app.models.base import utc_now


class StatsService:
    """Aggregate analytics for the dashboard."""

    async def overview(self, session: AsyncSession, user_id: str) -> dict[str, object]:
        """Return high-level application metrics."""
        now = utc_now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        total = await session.scalar(
            select(func.count()).select_from(JobApplication).where(JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False))
        ) or 0
        this_week = await session.scalar(
            select(func.count()).select_from(JobApplication).where(JobApplication.user_id == user_id, JobApplication.created_at >= week_ago)
        ) or 0
        this_month = await session.scalar(
            select(func.count()).select_from(JobApplication).where(JobApplication.user_id == user_id, JobApplication.created_at >= month_ago)
        ) or 0
        grouped = await session.execute(
            select(JobApplication.status, func.count()).where(JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False)).group_by(JobApplication.status)
        )
        by_status = {status: count for status, count in grouped.all()}
        offers = by_status.get(ApplicationStatus.OFFER.value, 0)
        responses = sum(by_status.get(status, 0) for status in [
            ApplicationStatus.PHONE_SCREEN.value,
            ApplicationStatus.INTERVIEW.value,
            ApplicationStatus.TECHNICAL.value,
            ApplicationStatus.FINAL_ROUND.value,
            ApplicationStatus.OFFER.value,
            ApplicationStatus.REJECTED.value,
        ])
        interviews_next_7_days = await session.scalar(
            select(func.count()).select_from(JobApplication).where(
                JobApplication.user_id == user_id,
                JobApplication.interview_at >= now,
                JobApplication.interview_at <= now + timedelta(days=7),
            )
        ) or 0
        return {
            "total": total,
            "this_week": this_week,
            "this_month": this_month,
            "by_status": by_status,
            "acceptance_rate": offers / total if total else 0,
            "response_rate": responses / total if total else 0,
            "avg_response_days": 0,
            "streak": this_week,
            "interviews_next_7_days": interviews_next_7_days,
        }

    async def funnel(self, session: AsyncSession, user_id: str) -> list[dict[str, object]]:
        """Return status counts for a funnel chart."""
        overview = await self.overview(session, user_id)
        by_status = overview["by_status"]
        assert isinstance(by_status, dict)
        return [{"status": status.value, "count": by_status.get(status.value, 0)} for status in ApplicationStatus]

    async def timeline(self, session: AsyncSession, user_id: str) -> list[dict[str, object]]:
        """Return simple daily application counts."""
        rows = await session.execute(
            select(func.date(JobApplication.created_at), func.count())
            .where(JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False))
            .group_by(func.date(JobApplication.created_at))
            .order_by(func.date(JobApplication.created_at))
        )
        return [{"date": str(day), "count": count} for day, count in rows.all()]

    async def salary(self, session: AsyncSession, user_id: str) -> dict[str, float | None]:
        """Return salary range analysis."""
        row = await session.execute(
            select(func.min(JobApplication.salary_min), func.avg(JobApplication.salary_min), func.max(JobApplication.salary_max)).where(
                JobApplication.user_id == user_id,
                JobApplication.is_deleted.is_(False),
            )
        )
        min_salary, avg_salary, max_salary = row.one()
        return {"min": min_salary, "average": avg_salary, "max": max_salary}

    async def sources(self, session: AsyncSession, user_id: str) -> list[dict[str, object]]:
        """Return application counts by source."""
        rows = await session.execute(
            select(JobApplication.source, func.count())
            .where(JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False))
            .group_by(JobApplication.source)
        )
        return [{"source": source or "Unknown", "count": count} for source, count in rows.all()]


stats_service = StatsService()

