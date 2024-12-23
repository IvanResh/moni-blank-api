import asyncio
from argparse import ArgumentParser

from structlog import get_logger

from db.db import get_db_pool
from db.db_context import DbContext
from domain import AccountDb, AccountRepository
from settings import get_settings
from utils.healthcheck import Healthcheck, init

logger = get_logger(__name__)


class AccountsCreator:

    def __init__(
        self,
        name_prefix: str,
        account_repository: AccountRepository,
    ) -> None:
        self._name_prefix = name_prefix

        self._account_repository = account_repository

    async def run_creator(self) -> None:
        await self._run_creator()

    async def _run_creator(self) -> None:
        counter = 0
        while True:
            counter += 1

            name = f"{self._name_prefix}:Name{counter}"
            await self._account_repository.insert_account(
                AccountDb(name=name),
            )
            logger.debug(f"Created new account {name}. Sleeping..")
            await asyncio.sleep(5)


async def run(
    name_prefix: str,
) -> None:
    settings = get_settings()
    init(
        sentry_dsn=settings.sentry_dsn,
        environment=settings.environment,
    )

    db_pool = await get_db_pool(
        dsn=settings.db_dsn,
        min_size=2,
        max_size=2,
    )

    db_context = DbContext(db_pool=db_pool)

    account_repository = AccountRepository(db_context=db_context)

    creator = AccountsCreator(
        name_prefix=name_prefix,
        account_repository=account_repository,
    )

    healthcheck = Healthcheck(8000)

    try:
        await healthcheck.start()
        await creator.run_creator()
    finally:
        logger.debug("Shutting down..")
        healthcheck.stop()
        await db_pool.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--name-prefix",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    logger.info(f"{args}")

    asyncio.run(
        run(
            name_prefix=args.name_prefix,
        ),
    )
