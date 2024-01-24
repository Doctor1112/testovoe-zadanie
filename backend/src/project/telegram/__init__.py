from aiogram import Bot, Dispatcher, enums

from project.settings import settings
from .utils.storage import DBStorage

bot = Bot(token=settings.BOT_TOKEN, parse_mode=enums.ParseMode.HTML)
Bot.set_current(bot)
dp = Dispatcher(bot=bot, storage=DBStorage())

from . import middlewares
from . import handlers
