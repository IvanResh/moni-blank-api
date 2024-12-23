from asyncio import CancelledError as AsyncioCancelledError
from typing import Callable

from aiohttp import web
from aiohttp.abc import Request


@web.middleware
async def suppress_cancelled_error_middleware(
    request: Request,
    handler: Callable,
) -> web.StreamResponse:
    """Suppress CancelledError and replace it with HTTPRequestTimeoutError."""
    try:
        return await handler(request)
    except AsyncioCancelledError as exc:
        raise web.HTTPRequestTimeout(text=str(exc))
