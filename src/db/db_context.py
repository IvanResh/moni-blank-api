from contextlib import asynccontextmanager
from typing import AsyncIterator

from asyncpg import Connection, Pool


class DbContext:
    def __init__(self, db_pool: Pool) -> None:
        self._db_pool = db_pool
        self._connection: Connection | None = None

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[Connection]:
        if self._connection and not self._connection.is_closed():
            yield self._connection
        else:
            async with self._db_pool.acquire() as connection:
                yield connection

    @asynccontextmanager
    async def start_transaction(self, isolation: str = None) -> None:
        if self._connection and not self._connection.is_closed():
            yield self._connection
            return
        self._connection: Connection = await self._db_pool.acquire()
        tr = self._connection.transaction(isolation=isolation)
        await tr.start()
        try:
            yield tr
        except:  # noqa: E722
            await tr.rollback()
            raise
        else:
            await tr.commit()
        finally:
            if self._connection:
                await self._db_pool.release(self._connection)
                self._connection = None

    async def close(self) -> None:
        if self._connection:
            await self._db_pool.release(self._connection)
        await self._db_pool.close()
