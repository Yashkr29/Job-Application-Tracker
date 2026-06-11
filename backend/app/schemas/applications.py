from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.application import ApplicationStatus, NoteType, Priority


class TagRead(BaseModel):
    """Tag response."""

    id: str
    name: str
    color: str

    model_config = {"from_attributes": True}


class StatusHistoryRead(BaseModel):
    """Status history response."""

    id: str
    from_status: str | None
    to_status: str
    note: str | None
    changed_at: datetime

    model_config = {"from_attributes": True}


class NoteRead(BaseModel):
    """Application note response."""

    id: str
    type: str
    body: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationBase(BaseModel):
    """Shared application fields."""

    title: str = Field(min_length=1, max_length=180)
    company: str = Field(min_length=1, max_length=180)
    location: str | None = None
    source: str | None = None
    job_url: str | None = None
    description: str | None = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    priority: Priority = Priority.MEDIUM
    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    applied_at: date | None = None
    follow_up_date: date | None = None
    interview_at: datetime | None = None
    offer_deadline: datetime | None = None


class ApplicationCreate(ApplicationBase):
    """Application create payload."""


class ApplicationUpdate(BaseModel):
    """Application update payload."""

    title: str | None = Field(default=None, min_length=1, max_length=180)
    company: str | None = Field(default=None, min_length=1, max_length=180)
    location: str | None = None
    source: str | None = None
    job_url: str | None = None
    description: str | None = None
    status: ApplicationStatus | None = None
    priority: Priority | None = None
    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    applied_at: date | None = None
    follow_up_date: date | None = None
    interview_at: datetime | None = None
    offer_deadline: datetime | None = None


class StatusUpdate(BaseModel):
    """Quick status update payload."""

    status: ApplicationStatus
    note: str | None = None


class ApplicationRead(BaseModel):
    """Application response."""

    id: str
    title: str
    company: str
    location: str | None
    source: str | None
    job_url: str | None
    description: str | None
    status: str
    priority: str
    salary_min: float | None
    salary_max: float | None
    currency: str
    applied_at: date | None
    follow_up_date: date | None
    interview_at: datetime | None
    offer_deadline: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationDetail(ApplicationRead):
    """Application detail response."""

    status_history: list[StatusHistoryRead] = []
    notes: list[NoteRead] = []
    tags: list[TagRead] = []


class ApplicationList(BaseModel):
    """Paginated application list."""

    items: list[ApplicationRead]
    total: int
    page: int
    limit: int


class NoteCreate(BaseModel):
    """Note create payload."""

    type: NoteType = NoteType.GENERAL
    body: str = Field(min_length=1)


class NoteUpdate(BaseModel):
    """Note update payload."""

    type: NoteType | None = None
    body: str | None = Field(default=None, min_length=1)


class TagCreate(BaseModel):
    """Tag create payload."""

    name: str = Field(min_length=1, max_length=80)
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")


class ContactCreate(BaseModel):
    """Contact create payload."""

    name: str = Field(min_length=1, max_length=160)
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    role: str | None = None
    notes: str | None = None


class ContactUpdate(BaseModel):
    """Contact update payload."""

    name: str | None = Field(default=None, min_length=1, max_length=160)
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    role: str | None = None
    notes: str | None = None


class ContactRead(ContactCreate):
    """Contact response."""

    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeRead(BaseModel):
    """Resume response."""

    id: str
    filename: str
    storage_path: str
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}

