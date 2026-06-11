from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy import select

from app.models.application import ApplicationResume, Resume
from app.models.base import utc_now
from app.routers.deps import CurrentUserDep, SessionDep
from app.schemas.applications import ResumeRead
from app.schemas.common import ApiResponse
from app.services.application_service import application_service
from app.services.storage_service import storage_service

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/", response_model=ApiResponse[ResumeRead])
async def upload_resume(
    session: SessionDep,
    current_user: CurrentUserDep,
    file: UploadFile = File(...),
) -> ApiResponse[ResumeRead]:
    """Upload a PDF resume."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF uploads are allowed")
    storage_path = await storage_service.upload_resume(current_user.id, file)
    resume = Resume(user_id=current_user.id, filename=file.filename or "resume.pdf", storage_path=storage_path)
    session.add(resume)
    await session.commit()
    await session.refresh(resume)
    return ApiResponse(data=ResumeRead.model_validate(resume), message="Resume uploaded")


@router.get("/", response_model=ApiResponse[list[ResumeRead]])
async def list_resumes(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[ResumeRead]]:
    """List resume versions."""
    result = await session.scalars(select(Resume).where(Resume.user_id == current_user.id, Resume.is_deleted.is_(False)))
    return ApiResponse(data=[ResumeRead.model_validate(resume) for resume in result])


@router.delete("/{resume_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_resume(resume_id: str, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, bool]]:
    """Soft-delete a resume."""
    resume = await session.scalar(select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id))
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    resume.is_deleted = True
    resume.deleted_at = utc_now()
    await session.commit()
    return ApiResponse(data={"deleted": True}, message="Resume deleted")


@router.post("/applications/{application_id}/{resume_id}", response_model=ApiResponse[dict[str, bool]])
async def link_resume(
    application_id: str,
    resume_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Link a resume to an application."""
    await application_service.get(session, current_user.id, application_id)
    resume = await session.scalar(select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id, Resume.is_deleted.is_(False)))
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    exists = await session.scalar(
        select(ApplicationResume).where(ApplicationResume.application_id == application_id, ApplicationResume.resume_id == resume_id)
    )
    if not exists:
        session.add(ApplicationResume(application_id=application_id, resume_id=resume_id, user_id=current_user.id))
        await session.commit()
    return ApiResponse(data={"linked": True}, message="Resume linked")

