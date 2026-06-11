from datetime import date
from typing import Literal

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import Response

from app.routers.deps import CurrentUserDep, SessionDep
from app.schemas.applications import (
    ApplicationCreate,
    ApplicationDetail,
    ApplicationList,
    ApplicationRead,
    ApplicationUpdate,
    NoteCreate,
    NoteRead,
    NoteUpdate,
    StatusUpdate,
)
from app.schemas.common import ApiResponse
from app.services.application_service import application_service

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApiResponse[ApplicationRead])
async def create_application(
    payload: ApplicationCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[ApplicationRead]:
    """Create a job application."""
    app = await application_service.create(session, current_user.id, payload)
    return ApiResponse(data=ApplicationRead.model_validate(app), message="Application created")


@router.get("/", response_model=ApiResponse[ApplicationList])
async def list_applications(
    session: SessionDep,
    current_user: CurrentUserDep,
    status: str | None = None,
    search: str | None = None,
    company: str | None = None,
    location: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    salary_min: float | None = None,
    sort_by: str = "created_at",
    order: Literal["asc", "desc"] = "desc",
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
) -> ApiResponse[ApplicationList]:
    """List applications with filters, sorting, and pagination."""
    items, total = await application_service.list(
        session,
        current_user.id,
        status_filter=status,
        search=search,
        company=company,
        location=location,
        date_from=date_from,
        date_to=date_to,
        salary_min=salary_min,
        sort_by=sort_by,
        order=order,
        page=page,
        limit=limit,
    )
    return ApiResponse(
        data=ApplicationList(
            items=[ApplicationRead.model_validate(item) for item in items],
            total=total,
            page=page,
            limit=limit,
        )
    )


@router.get("/export")
async def export_applications(session: SessionDep, current_user: CurrentUserDep) -> Response:
    """Download applications as CSV."""
    csv_data = await application_service.export_csv(session, current_user.id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=applications.csv"},
    )


@router.post("/import", response_model=ApiResponse[dict[str, int]])
async def import_applications(
    session: SessionDep,
    current_user: CurrentUserDep,
    file: UploadFile = File(...),
) -> ApiResponse[dict[str, int]]:
    """Bulk import applications from CSV."""
    imported = await application_service.import_csv(session, current_user.id, file)
    return ApiResponse(data={"imported": imported}, message="Applications imported")


@router.get("/upcoming", response_model=ApiResponse[list[ApplicationRead]])
async def upcoming_applications(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[ApplicationRead]]:
    """Return interviews in the next 7 days."""
    apps = await application_service.upcoming(session, current_user.id)
    return ApiResponse(data=[ApplicationRead.model_validate(app) for app in apps])


@router.get("/{application_id}", response_model=ApiResponse[ApplicationDetail])
async def get_application(
    application_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[ApplicationDetail]:
    """Get one application with notes and status history."""
    app = await application_service.get(session, current_user.id, application_id)
    return ApiResponse(data=application_service.to_detail(app))


@router.put("/{application_id}", response_model=ApiResponse[ApplicationRead])
async def update_application(
    application_id: str,
    payload: ApplicationUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[ApplicationRead]:
    """Update an application."""
    app = await application_service.update(session, current_user.id, application_id, payload)
    return ApiResponse(data=ApplicationRead.model_validate(app), message="Application updated")


@router.delete("/{application_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_application(
    application_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Soft-delete an application."""
    await application_service.soft_delete(session, current_user.id, application_id)
    return ApiResponse(data={"deleted": True}, message="Application deleted")


@router.patch("/{application_id}/status", response_model=ApiResponse[ApplicationRead])
async def update_application_status(
    application_id: str,
    payload: StatusUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[ApplicationRead]:
    """Quick-update an application status."""
    app = await application_service.update_status(session, current_user.id, application_id, payload)
    return ApiResponse(data=ApplicationRead.model_validate(app), message="Status updated")


@router.post("/{application_id}/notes", response_model=ApiResponse[NoteRead])
async def add_note(
    application_id: str,
    payload: NoteCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[NoteRead]:
    """Add an application note."""
    note = await application_service.add_note(session, current_user.id, application_id, payload)
    return ApiResponse(data=NoteRead.model_validate(note), message="Note added")


@router.get("/{application_id}/notes", response_model=ApiResponse[list[NoteRead]])
async def list_notes(
    application_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[list[NoteRead]]:
    """List application notes."""
    notes = await application_service.list_notes(session, current_user.id, application_id)
    return ApiResponse(data=[NoteRead.model_validate(note) for note in notes])


@router.put("/{application_id}/notes/{note_id}", response_model=ApiResponse[NoteRead])
async def update_note(
    application_id: str,
    note_id: str,
    payload: NoteUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[NoteRead]:
    """Edit an application note."""
    _ = application_id
    note = await application_service.update_note(session, current_user.id, note_id, payload)
    return ApiResponse(data=NoteRead.model_validate(note), message="Note updated")


@router.delete("/{application_id}/notes/{note_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_note(
    application_id: str,
    note_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Delete an application note."""
    _ = application_id
    await application_service.delete_note(session, current_user.id, note_id)
    return ApiResponse(data={"deleted": True}, message="Note deleted")

