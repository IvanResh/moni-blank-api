from asyncpg import Record

from db.db_context import DbContext
from domain import AccountDb


class AccountRepository:
    def __init__(self, db_context: DbContext) -> None:
        self._db_context = db_context

    async def get_account_by_id(
        self,
        id: int,
    ) -> Record | None:
        query = """
            select a.*
            from account a
            where a.id = $1
            limit 1;
        """

        async with self._db_context.get_connection() as connection:
            return await connection.fetchrow(query, id)

    async def insert_account(
        self,
        item: AccountDb,
    ) -> AccountDb | None:
        query = """
            insert into account (name)
            values ($1)
            on conflict do nothing;
        """

        async with self._db_context.get_connection() as connection:
            row = await connection.fetchrow(query, item.name)
        if not row:
            return None
        return AccountDb.parse_obj(row)
