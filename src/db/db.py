from datetime import datetime
from decimal import Decimal

import asyncpg
import ujson
from asyncpg import Connection, Pool

from helpers import BaseModel


async def _init_connection(connection: Connection) -> None:
    await connection.set_type_codec(
        "json",
        encoder=_encoder,
        decoder=ujson.loads,
        schema="pg_catalog",
    )
    await connection.set_type_codec(
        "jsonb",
        encoder=_encoder,
        decoder=ujson.loads,
        schema="pg_catalog",
    )


async def get_db_pool(testing: bool = False, **kwargs) -> Pool:
    """Creates postgres pool."""
    kwargs.setdefault("command_timeout", 10)
    if testing:
        kwargs.setdefault("server_settings", {"jit": "off"})
    return await asyncpg.create_pool(**kwargs, init=_init_connection)


async def get_pgbouncer_pool(testing: bool = False, **kwargs) -> Pool:
    """Creates postgres pool."""
    kwargs.setdefault("command_timeout", 10)
    if testing:
        kwargs.setdefault("server_settings", {"jit": "off"})
    return await asyncpg.create_pool(
        **kwargs,
        init=_init_connection,
        statement_cache_size=0,
    )


def _encoder(obj):
    return ujson.dumps(obj, default=default_handler)


def default_handler(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return str(obj)
    if isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError
