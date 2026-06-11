from __future__ import annotations

from datetime import date, timedelta
from typing import Literal

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import Select, and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.application import (
    ApplicationNote,
    ApplicationStatus,
    ApplicationTag,
    Contact,
    JobApplication,
    StatusHistory,
)
from app.models.base import utc_now
from app.schemas.applications import (
    ApplicationCreate,
    ApplicationDetail,
    ApplicationRead,
    ApplicationUpdate,
    NoteCreate,
    NoteRead,
    NoteUpdate,
    StatusHistoryRead,
    StatusUpdate,
    TagRead,
)
from app.utils.csv_handler import applications_to_csv, parse_applications_csv


class ApplicationService:
    """Business logic for applications and related records."""

    async def create(self, session: AsyncSession, user_id: str, payload: ApplicationCreate) -> JobApplication:
        """Create an application and initial status history."""
        app = JobApplication(user_id=user_id, **payload.model_dump())
        session.add(app)
        await session.flush()
        session.add(StatusHistory(application_id=app.id, user_id=user_id, from_status=None, to_status=app.status))
        await session.commit()
        await session.refresh(app)
        return app

    async def list(
        self,
        session: AsyncSession,
        user_id: str,
        *,
        status_filter: str | None = None,
        search: str | None = None,
        company: str | None = None,
        location: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        salary_min: float | None = None,
        sort_by: str = "created_at",
        order: Literal["asc", "desc"] = "desc",
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[JobApplication], int]:
        """List applications with filters and pagination."""
        filters = [JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False)]
        if status_filter:
            filters.append(JobApplication.status == status_filter)
        if search:
            term = f"%{search}%"
            filters.append(or_(JobApplication.title.ilike(term), JobApplication.company.ilike(term)))
        if company:
            filters.append(JobApplication.company.ilike(f"%{company}%"))
        if location:
            filters.append(JobApplication.location.ilike(f"%{location}%"))
        if date_from:
            filters.append(JobApplication.applied_at >= date_from)
        if date_to:
            filters.append(JobApplication.applied_at <= date_to)
        if salary_min is not None:
            filters.append(or_(JobApplication.salary_min >= salary_min, JobApplication.salary_max >= salary_min))

        sort_column = getattr(JobApplication, sort_by, JobApplication.created_at)
        sort_expr = sort_column.asc() if order == "asc" else sort_column.desc()
        query = select(JobApplication).where(and_(*filters)).order_by(sort_expr).offset((page - 1) * limit).limit(limit)
        count_query = select(func.count()).select_from(JobApplication).where(and_(*filters))
        total = await session.scalar(count_query) or 0
        result = await session.scalars(query)
        return list(result), total

    async def get(self, session: AsyncSession, user_id: str, application_id: str) -> JobApplication:
        """Get an application owned by a user."""
        app = await session.scalar(
            select(JobApplication)
            .options(
                selectinload(JobApplication.status_history),
                selectinload(JobApplication.notes),
                selectinload(JobApplication.tag_links).selectinload(ApplicationTag.tag),
            )
            .where(JobApplication.id == application_id, JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False))
        )
        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        return app

    async def update(self, session: AsyncSession, user_id: str, application_id: str, payload: ApplicationUpdate) -> JobApplication:
        """Update an application and log status changes."""
        app = await self.get(session, user_id, application_id)
        data = payload.model_dump(exclude_unset=True)
        old_status = app.status
        for key, value in data.items():
            setattr(app, key, value)
        if "status" in data and data["status"] != old_status:
            session.add(StatusHistory(application_id=app.id, user_id=user_id, from_status=old_status, to_status=data["status"]))
        await session.commit()
        await session.refresh(app)
        return app

    async def update_status(self, session: AsyncSession, user_id: str, application_id: str, payload: StatusUpdate) -> JobApplication:
        """Quick-update application status."""
        app = await self.get(session, user_id, application_id)
        old_status = app.status
        app.status = payload.status.value
        if old_status != app.status:
            session.add(
                StatusHistory(
                    application_id=app.id,
                    user_id=user_id,
                    from_status=old_status,
                    to_status=app.status,
                    note=payload.note,
                )
            )
        await session.commit()
        await session.refresh(app)
        return app

    async def soft_delete(self, session: AsyncSession, user_id: str, application_id: str) -> None:
        """Soft-delete an application."""
        app = await self.get(session, user_id, application_id)
        app.is_deleted = True
        app.deleted_at = utc_now()
        await session.commit()

    async def upcoming(self, session: AsyncSession, user_id: str) -> list[JobApplication]:
        """Return interviews scheduled in the next 7 days."""
        now = utc_now()
        end = now + timedelta(days=7)
        result = await session.scalars(
            select(JobApplication).where(
                JobApplication.user_id == user_id,
                JobApplication.is_deleted.is_(False),
                JobApplication.interview_at >= now,
                JobApplication.interview_at <= end,
            )
        )
        return list(result)

    async def export_csv(self, session: AsyncSession, user_id: str) -> str:
        """Export applications to CSV."""
        result = await session.scalars(
            select(JobApplication).where(JobApplication.user_id == user_id, JobApplication.is_deleted.is_(False))
        )
        return applications_to_csv(list(result))

    async def import_csv(self, session: AsyncSession, user_id: str, file: UploadFile) -> int:
        """Import applications from CSV."""
        content = (await file.read()).decode("utf-8")
        rows = parse_applications_csv(content)
        for row in rows:
            app = JobApplication(
                user_id=user_id,
                title=row["title"],
                company=row["company"],
                location=row.get("location") or None,
                source=row.get("source") or None,
                status=row.get("status") or ApplicationStatus.SAVED.value,
                priority=row.get("priority") or "medium",
                salary_min=float(row["salary_min"]) if row.get("salary_min") else None,
                salary_max=float(row["salary_max"]) if row.get("salary_max") else None,
                currency=row.get("currency") or "INR",
            )
            session.add(app)
        await session.commit()
        return len(rows)

    async def add_note(self, session: AsyncSession, user_id: str, application_id: str, payload: NoteCreate) -> ApplicationNote:
        """Add a note to an application."""
        await self.get(session, user_id, application_id)
        note = ApplicationNote(application_id=application_id, user_id=user_id, type=payload.type.value, body=payload.body)
        session.add(note)
        await session.commit()
        await session.refresh(note)
        return note

    async def list_notes(self, session: AsyncSession, user_id: str, application_id: str) -> list[ApplicationNote]:
        """List notes for an application."""
        await self.get(session, user_id, application_id)
        result = await session.scalars(
            select(ApplicationNote).where(
                ApplicationNote.application_id == application_id,
                ApplicationNote.user_id == user_id,
                ApplicationNote.is_deleted.is_(False),
            )
        )
        return list(result)

    async def update_note(self, session: AsyncSession, user_id: str, note_id: str, payload: NoteUpdate) -> ApplicationNote:
        """Update an application note."""
        note = await session.scalar(
            select(ApplicationNote).where(ApplicationNote.id == note_id, ApplicationNote.user_id == user_id, ApplicationNote.is_deleted.is_(False))
        )
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(note, key, value.value if hasattr(value, "value") else value)
        await session.commit()
        await session.refresh(note)
        return note

    async def delete_note(self, session: AsyncSession, user_id: str, note_id: str) -> None:
        """Soft-delete an application note."""
        note = await session.scalar(select(ApplicationNote).where(ApplicationNote.id == note_id, ApplicationNote.user_id == user_id))
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        note.is_deleted = True
        note.deleted_at = utc_now()
        await session.commit()

    def to_detail(self, app: JobApplication) -> ApplicationDetail:
        """Convert an application ORM object to a detail schema."""
        base = ApplicationRead.model_validate(app).model_dump()
        return ApplicationDetail(
            **base,
            status_history=[StatusHistoryRead.model_validate(item) for item in app.status_history],
            notes=[NoteRead.model_validate(note) for note in app.notes if not note.is_deleted],
            tags=[TagRead.model_validate(link.tag) for link in app.tag_links],
        )


application_service = ApplicationService()


def owned_contact_query(user_id: str, contact_id: str | None = None) -> Select[tuple[Contact]]:
    """Build an owned contact query."""
    query = select(Contact).where(Contact.user_id == user_id, Contact.is_deleted.is_(False))
    if contact_id:
        query = query.where(Contact.id == contact_id)
    return query
