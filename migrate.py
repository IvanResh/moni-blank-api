#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
from time import sleep
from typing import Callable

from structlog import get_logger
from yoyo import get_backend, read_migrations
from yoyo.backends import DatabaseBackend
from yoyo.migrations import MigrationList

from settings import Settings, get_settings

logger = get_logger(name="migrate")

DB_MIGRATIONS = "src/db/migrations"

TAction = Callable[[DatabaseBackend, MigrationList], None]


def _apply(backend, migrations):
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def _rollback(backend, migrations):
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))


def _rollback_one(backend, migrations):
    with backend.lock():
        migrations = backend.to_rollback(migrations)
        for migration in migrations:
            backend.rollback_one(migration)
            break


def run(settings: Settings, action: TAction) -> None:
    logger.info("Apply migrations", settings=settings)

    logger.info(f"Apply migrations for path {DB_MIGRATIONS} dsn {settings.db_dsn}...")
    backend = wait_backend(settings.db_dsn)
    migrations = read_migrations(DB_MIGRATIONS)
    action(backend, migrations)
    logger.info(f"Migrations for path {DB_MIGRATIONS} dsn {settings.db_dsn} applied")


def wait_backend(db_dsn: str, attempts: int = 12, pause: float = 5.0):
    while True:
        try:
            return get_backend(db_dsn)
        except Exception as exc:  # pylint: disable=broad-except
            if "Connection refused" in str(exc):
                attempts -= 1
                if attempts > 0:
                    logger.warning(
                        "Database at dsn {dsn} refuses connections",
                        dsn=db_dsn,
                    )
                    sleep(pause)
                    continue
            raise


def cli() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
    )

    parser = ArgumentParser(description="Apply migrations")
    parser.add_argument("--rollback", action="store_true", help="Rollback migrations")
    parser.add_argument(
        "--rollback-one",
        action="store_true",
        help="Rollback one migration",
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.rollback:
        action = _rollback
    elif args.rollback_one:
        action = _rollback_one
    else:
        action = _apply
    run(settings, action)


if __name__ == "__main__":
    cli()
