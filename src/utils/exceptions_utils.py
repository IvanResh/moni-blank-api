import asyncio
from functools import wraps
from typing import Callable, Coroutine

from structlog import get_logger

logger = get_logger(__name__)


def retry(exc, attempts, delay) -> Callable:  # noqa: C901 too complex
    def deco(function: Callable) -> Callable:
        @wraps(function)
        async def wrapper(*args, **kwargs) -> Coroutine:
            attempt = 1
            while True:
                try:
                    return await function(*args, **kwargs)
                except exc:
                    logger.warning(f"Exc: {exc}. Retries: {attempt}")
                    if attempt < attempts:
                        attempt += 1
                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise

        return wrapper

    return deco
