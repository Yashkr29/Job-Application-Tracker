from typing import Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    """Standard successful API response."""

    success: bool = True
    data: DataT | None = None
    message: str = "OK"


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: str
    details: dict[str, object] | list[object] | None = None

