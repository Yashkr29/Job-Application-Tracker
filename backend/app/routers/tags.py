from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.models.application import ApplicationTag, Tag
from app.routers.deps import CurrentUserDep, SessionDep
from app.schemas.applications import TagCreate, TagRead
from app.schemas.common import ApiResponse
from app.services.application_service import application_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=ApiResponse[TagRead])
async def create_tag(payload: TagCreate, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[TagRead]:
    """Create a user tag."""
    tag = Tag(user_id=current_user.id, name=payload.name, color=payload.color)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return ApiResponse(data=TagRead.model_validate(tag), message="Tag created")


@router.get("/", response_model=ApiResponse[list[TagRead]])
async def list_tags(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[TagRead]]:
    """List user tags."""
    result = await session.scalars(select(Tag).where(Tag.user_id == current_user.id).order_by(Tag.name))
    return ApiResponse(data=[TagRead.model_validate(tag) for tag in result])


@router.delete("/{tag_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_tag(tag_id: str, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, bool]]:
    """Delete a user tag."""
    tag = await session.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    await session.delete(tag)
    await session.commit()
    return ApiResponse(data={"deleted": True}, message="Tag deleted")


@router.post("/applications/{application_id}/{tag_id}", response_model=ApiResponse[dict[str, bool]])
async def attach_tag(
    application_id: str,
    tag_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Attach a tag to an application."""
    await application_service.get(session, current_user.id, application_id)
    tag = await session.scalar(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    exists = await session.scalar(select(ApplicationTag).where(ApplicationTag.application_id == application_id, ApplicationTag.tag_id == tag_id))
    if not exists:
        session.add(ApplicationTag(application_id=application_id, tag_id=tag_id, user_id=current_user.id))
        await session.commit()
    return ApiResponse(data={"attached": True}, message="Tag attached")


@router.delete("/applications/{application_id}/{tag_id}", response_model=ApiResponse[dict[str, bool]])
async def remove_tag(
    application_id: str,
    tag_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[dict[str, bool]]:
    """Remove a tag from an application."""
    link = await session.scalar(
        select(ApplicationTag).where(
            ApplicationTag.application_id == application_id,
            ApplicationTag.tag_id == tag_id,
            ApplicationTag.user_id == current_user.id,
        )
    )
    if link:
        await session.delete(link)
        await session.commit()
    return ApiResponse(data={"removed": True}, message="Tag removed")

