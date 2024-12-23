from asyncio import Semaphore as AsyncioSemaphore
from asyncio import gather as asyncio_gather
from typing import Any, Coroutine


async def gather_with_concurrency(n, *tasks) -> tuple[Any]:
    semaphore = AsyncioSemaphore(n)

    async def sem_task(task) -> Coroutine:
        async with semaphore:
            return await task

    return await asyncio_gather(*(sem_task(task) for task in tasks))
