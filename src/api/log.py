from aiohttp.abc import AbstractAccessLogger
from structlog import get_logger

access_logger = get_logger(name="access_log")


class RequestLogger(AbstractAccessLogger):
    """Logger for aiohttp requests."""

    def log(self, request, response, time) -> None:
        """Emit log to logger."""
        if request.path.startswith("/healthcheck"):
            return

        if request.headers.get("allowLogging") == "false":
            return
        access_logger.info(
            f"{request.method} {request.path} {response.status} in {time} sec, request_id {request.headers.get('requestId')}",
        )
