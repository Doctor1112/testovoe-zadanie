from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import get_i18n

from project.db.models import User
from project.settings import settings
from project.telegram import dp
from project.telegram.handlers.messages.private.commands import start
from project.telegram.utils.handler import handler


@dp.message(Command('restart'), lambda _: settings.DEBUG)
@handler
async def restart(message: types.Message, user: User, state: FSMContext):
    await user.delete()
    await start(message, state=state)


@dp.message(Command('locales'), lambda _: settings.DEBUG)
@handler
async def locales(_: types.Message):
    i18n = get_i18n()
    i18n.reload()
