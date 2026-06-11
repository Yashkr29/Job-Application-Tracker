import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

logger = logging.getLogger("job_tracker.requests")


async def request_logging_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Log each request with structured fields."""
    started = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round((time.perf_counter() - started) * 1000, 2),
        },
    )
    return response

