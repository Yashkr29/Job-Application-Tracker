from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import Date, DateTime, Float, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin, UUIDMixin, utc_now


class ApplicationStatus(StrEnum):
    """Job application pipeline stages."""

    SAVED = "SAVED"
    APPLIED = "APPLIED"
    PHONE_SCREEN = "PHONE_SCREEN"
    INTERVIEW = "INTERVIEW"
    TECHNICAL = "TECHNICAL"
    FINAL_ROUND = "FINAL_ROUND"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    GHOSTED = "GHOSTED"


class Priority(StrEnum):
    """Application priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DREAM = "dream"


class NoteType(StrEnum):
    """Application note categories."""

    GENERAL = "general"
    INTERVIEW_PREP = "interview_prep"
    FOLLOW_UP = "follow_up"
    FEEDBACK = "feedback"
    OFFER_NEGOTIATION = "offer_negotiation"


class JobApplication(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Tracked job application."""

    __tablename__ = "job_applications"
    __table_args__ = (
        Index("ix_job_applications_user_status", "user_id", "status"),
        Index("ix_job_applications_company_title", "company", "title"),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    company: Mapped[str] = mapped_column(String(180), nullable=False)
    location: Mapped[str | None] = mapped_column(String(180), nullable=True)
    source: Mapped[str | None] = mapped_column(String(120), nullable=True)
    job_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default=ApplicationStatus.SAVED.value, index=True, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default=Priority.MEDIUM.value, nullable=False)
    salary_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    applied_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    interview_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    offer_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status_history: Mapped[list["StatusHistory"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="StatusHistory.created_at",
    )
    notes: Mapped[list["ApplicationNote"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    tag_links: Mapped[list["ApplicationTag"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    resume_links: Mapped[list["ApplicationResume"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    contact_links: Mapped[list["ApplicationContact"]] = relationship(back_populates="application", cascade="all, delete-orphan")


class StatusHistory(UUIDMixin, TimestampMixin, Base):
    """Application status change log."""

    __tablename__ = "status_history"

    application_id: Mapped[str] = mapped_column(ForeignKey("job_applications.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    from_status: Mapped[str | None] = mapped_column(String(40), nullable=True)
    to_status: Mapped[str] = mapped_column(String(40), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    application: Mapped[JobApplication] = relationship(back_populates="status_history")


class ApplicationNote(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Note attached to an application."""

    __tablename__ = "application_notes"

    application_id: Mapped[str] = mapped_column(ForeignKey("job_applications.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(40), default=NoteType.GENERAL.value, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    application: Mapped[JobApplication] = relationship(back_populates="notes")


class Tag(UUIDMixin, TimestampMixin, Base):
    """User-defined application tag."""

    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_tags_user_name"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)

    application_links: Mapped[list["ApplicationTag"]] = relationship(back_populates="tag", cascade="all, delete-orphan")


class ApplicationTag(UUIDMixin, TimestampMixin, Base):
    """Application/tag junction row."""

    __tablename__ = "application_tags"
    __table_args__ = (UniqueConstraint("application_id", "tag_id", name="uq_application_tags_application_tag"),)

    application_id: Mapped[str] = mapped_column(ForeignKey("job_applications.id", ondelete="CASCADE"), index=True)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    application: Mapped[JobApplication] = relationship(back_populates="tag_links")
    tag: Mapped[Tag] = relationship(back_populates="application_links")


class Contact(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Recruiter or interviewer contact."""

    __tablename__ = "contacts"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    company: Mapped[str | None] = mapped_column(String(180), nullable=True)
    role: Mapped[str | None] = mapped_column(String(120), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    application_links: Mapped[list["ApplicationContact"]] = relationship(back_populates="contact", cascade="all, delete-orphan")


class ApplicationContact(UUIDMixin, TimestampMixin, Base):
    """Application/contact junction row."""

    __tablename__ = "application_contacts"
    __table_args__ = (UniqueConstraint("application_id", "contact_id", name="uq_application_contacts_application_contact"),)

    application_id: Mapped[str] = mapped_column(ForeignKey("job_applications.id", ondelete="CASCADE"), index=True)
    contact_id: Mapped[str] = mapped_column(ForeignKey("contacts.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    application: Mapped[JobApplication] = relationship(back_populates="contact_links")
    contact: Mapped[Contact] = relationship(back_populates="application_links")


class Resume(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Uploaded resume version."""

    __tablename__ = "resumes"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)

    application_links: Mapped[list["ApplicationResume"]] = relationship(back_populates="resume", cascade="all, delete-orphan")


class ApplicationResume(UUIDMixin, TimestampMixin, Base):
    """Application/resume junction row."""

    __tablename__ = "application_resumes"
    __table_args__ = (UniqueConstraint("application_id", "resume_id", name="uq_application_resumes_application_resume"),)

    application_id: Mapped[str] = mapped_column(ForeignKey("job_applications.id", ondelete="CASCADE"), index=True)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    application: Mapped[JobApplication] = relationship(back_populates="resume_links")
    resume: Mapped[Resume] = relationship(back_populates="application_links")

