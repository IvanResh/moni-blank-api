from functools import partial

from aiohttp import web
from aiohttp_apispec import docs, querystring_schema, response_schema

from application import GetAccountHandler, GetAccountQuery
from domain import AccountNotFoundException

from . import schemas

docs = partial(docs, tags=["Account"])


@docs()
@querystring_schema(schemas.GetAccountRequestSchema)
@response_schema(schemas.GetAccountResponseSchema)
async def get_account_handler(request: web.Request) -> web.Response:
    handler: GetAccountHandler = request.app["get_account_handler"]()

    try:
        response = await handler.handle(
            GetAccountQuery(
                id=request["querystring"]["id"],
            ),
        )
    except AccountNotFoundException:
        return web.HTTPNotFound()

    return web.HTTPOk(
        body=schemas.GetAccountResponseSchema().dumps(response),
        content_type="application/json",
    )


routes = (
    web.get(
        "/api/v1/account/",
        get_account_handler,
        allow_head=False,
    ),
)
