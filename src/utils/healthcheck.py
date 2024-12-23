from asyncio import StreamWriter as AsyncioStreamWriter
from asyncio import start_server as asyncio_start_server

from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from structlog import get_logger

logger = get_logger(name="healthcheck")


def init(sentry_dsn: str, environment: str = "local") -> None:
    import sentry_sdk

    if sentry_dsn and environment != "local":
        sentry_sdk.init(
            sentry_dsn,
            traces_sample_rate=0.01,
            environment=environment,
            integrations=[
                AioHttpIntegration(),
            ],
        )


async def _handler(_, w: AsyncioStreamWriter) -> None:
    w.write(b"HTTP/1.1 200\nContent-Length: 0\n\n")
    await w.drain()


class Healthcheck:
    """Simple healthcheck server."""

    def __init__(self, port: int) -> None:
        self._port = port
        self._server = None

    async def start(self) -> None:
        """Start healthcheck server."""
        self._server = await asyncio_start_server(_handler, "0.0.0.0", self._port)
        logger.info(f"Healthcheck started at port {self._port}")

    def stop(self) -> None:
        """Stop healthcheck server."""
        if self._server:
            self._server.close()
            logger.info("Healthcheck stopped")
