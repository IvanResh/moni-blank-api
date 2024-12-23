import aiohttp_cors
import uvloop
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from structlog import get_logger

from api import log
from api.middlewares import suppress_cancelled_error_middleware
from api.routes import routes
from application import GetAccountHandler
from db.db import get_db_pool
from db.db_context import DbContext
from domain import AccountRepository
from settings import Settings, get_settings
from utils.healthcheck import init

logger = get_logger(__name__)


async def _setup_db(app: web.Application) -> None:
    app["db_pool"] = await get_db_pool(
        dsn=app["settings"].db_dsn,
        min_size=app["settings"].db_pool_min_size,
        max_size=app["settings"].db_pool_max_size,
        command_timeout=app["settings"].db_command_timeout,
        testing=app["settings"].testing,
    )


async def _setup_di(app: web.Application) -> None:

    def resolve_account_repository(
        db_context: DbContext | None = None,
    ) -> AccountRepository:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AccountRepository(db_context)

    app["account_repository"] = resolve_account_repository

    def resolve_get_account_handler(
        db_context: DbContext | None = None,
    ) -> GetAccountHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return GetAccountHandler(
            account_repository=app["account_repository"](db_context),
        )

    app["get_account_handler"] = resolve_get_account_handler


async def _close_db(app: web.Application) -> None:
    await app["db_pool"].close()


def get_app(settings: Settings) -> web.Application:
    init(sentry_dsn=settings.sentry_dsn, environment=settings.environment)

    app = web.Application(
        middlewares=[
            suppress_cancelled_error_middleware,
            validation_middleware,
            normalize_path_middleware(),
        ],
    )

    app["settings"] = settings
    app.add_routes(routes)

    app.on_startup.extend(
        [
            _setup_db,
            _setup_di,
        ],
    )
    app.on_cleanup.extend(
        [
            _close_db,
        ],
    )

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            ),
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)

    setup_aiohttp_apispec(
        app=app,
        title="Moni Blank API",
        version="v1",
        request_data_name="validated_data",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs/",
        securityDefinitions={
            "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"},
        },
    )
    return app


if __name__ == "__main__":
    logger.info("Starting..")
    settings = get_settings()
    if settings.environment == "prod":
        uvloop.install()
    app = get_app(settings)
    web.run_app(
        app,
        port=settings.web_port,
        access_log_class=log.RequestLogger,
    )
