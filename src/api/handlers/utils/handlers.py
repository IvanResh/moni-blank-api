from aiohttp import web
from aiohttp.abc import Request


async def healthcheck_handler(request: Request) -> web.Response:
    return web.HTTPOk()


routes = (
    web.get(
        "/healthcheck/",
        healthcheck_handler,
        allow_head=False,
    ),
)
