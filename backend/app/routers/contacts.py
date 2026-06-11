from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.models.application import ApplicationContact, Contact, JobApplication
from app.models.base import utc_now
from app.routers.deps import CurrentUserDep, SessionDep
from app.schemas.applications import ApplicationRead, ContactCreate, ContactRead, ContactUpdate
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ApiResponse[ContactRead])
async def create_contact(payload: ContactCreate, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[ContactRead]:
    """Create a contact."""
    contact = Contact(user_id=current_user.id, **payload.model_dump())
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return ApiResponse(data=ContactRead.model_validate(contact), message="Contact created")


@router.get("/", response_model=ApiResponse[list[ContactRead]])
async def list_contacts(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[ContactRead]]:
    """List contacts."""
    result = await session.scalars(select(Contact).where(Contact.user_id == current_user.id, Contact.is_deleted.is_(False)))
    return ApiResponse(data=[ContactRead.model_validate(contact) for contact in result])


@router.get("/{contact_id}", response_model=ApiResponse[ContactRead])
async def get_contact(contact_id: str, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[ContactRead]:
    """Get one contact."""
    contact = await session.scalar(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id, Contact.is_deleted.is_(False)))
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return ApiResponse(data=ContactRead.model_validate(contact))


@router.put("/{contact_id}", response_model=ApiResponse[ContactRead])
async def update_contact(
    contact_id: str,
    payload: ContactUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[ContactRead]:
    """Update a contact."""
    contact = await session.scalar(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id, Contact.is_deleted.is_(False)))
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)
    await session.commit()
    await session.refresh(contact)
    return ApiResponse(data=ContactRead.model_validate(contact), message="Contact updated")


@router.delete("/{contact_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_contact(contact_id: str, session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, bool]]:
    """Soft-delete a contact."""
    contact = await session.scalar(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id))
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    contact.is_deleted = True
    contact.deleted_at = utc_now()
    await session.commit()
    return ApiResponse(data={"deleted": True}, message="Contact deleted")


@router.get("/{contact_id}/applications", response_model=ApiResponse[list[ApplicationRead]])
async def contact_applications(
    contact_id: str,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApiResponse[list[ApplicationRead]]:
    """List applications linked to a contact."""
    rows = await session.scalars(
        select(JobApplication)
        .join(ApplicationContact, ApplicationContact.application_id == JobApplication.id)
        .where(
            ApplicationContact.contact_id == contact_id,
            ApplicationContact.user_id == current_user.id,
            JobApplication.is_deleted.is_(False),
        )
    )
    return ApiResponse(data=[ApplicationRead.model_validate(app) for app in rows])

