from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination query params."""

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Return SQL offset."""
        return (self.page - 1) * self.limit

