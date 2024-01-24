from aiogram.client.session.middlewares.request_logging import RequestLogging

from project.telegram import dp, bot
from project.telegram.middlewares.i18n import DBI18nMiddleware
from project.telegram.middlewares.logging import LoggingMiddleware
from project.telegram.middlewares.users import UserMiddleware

# Hell yes, order is important. Be careful
bot.session.middleware(RequestLogging())
dp.update.outer_middleware(LoggingMiddleware())
dp.update.outer_middleware(UserMiddleware())
dp.update.outer_middleware(DBI18nMiddleware())
