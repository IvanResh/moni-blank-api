from .handlers.account import handlers as account_handlers
from .handlers.utils import handlers as utils_handlers

routes = (*account_handlers.routes, *utils_handlers.routes)
