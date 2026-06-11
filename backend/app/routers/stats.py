from fastapi import APIRouter

from app.routers.deps import CurrentUserDep, SessionDep
from app.schemas.common import ApiResponse
from app.services.stats_service import stats_service

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview", response_model=ApiResponse[dict[str, object]])
async def overview(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, object]]:
    """Return dashboard overview stats."""
    return ApiResponse(data=await stats_service.overview(session, current_user.id))


@router.get("/funnel", response_model=ApiResponse[list[dict[str, object]]])
async def funnel(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[dict[str, object]]]:
    """Return funnel chart stats."""
    return ApiResponse(data=await stats_service.funnel(session, current_user.id))


@router.get("/timeline", response_model=ApiResponse[list[dict[str, object]]])
async def timeline(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[dict[str, object]]]:
    """Return timeline stats."""
    return ApiResponse(data=await stats_service.timeline(session, current_user.id))


@router.get("/salary", response_model=ApiResponse[dict[str, float | None]])
async def salary(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[dict[str, float | None]]:
    """Return salary analytics."""
    return ApiResponse(data=await stats_service.salary(session, current_user.id))


@router.get("/sources", response_model=ApiResponse[list[dict[str, object]]])
async def sources(session: SessionDep, current_user: CurrentUserDep) -> ApiResponse[list[dict[str, object]]]:
    """Return source breakdown stats."""
    return ApiResponse(data=await stats_service.sources(session, current_user.id))

