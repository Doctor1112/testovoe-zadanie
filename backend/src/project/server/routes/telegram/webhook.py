from aiogram import types, Bot
from fastapi import status
from loguru import logger

from project.server import app
from project.settings import settings
from project.telegram import dp


async def handle_update(update: types.Update):
    bot = Bot.get_current()
    try:
        return await dp.feed_update(bot, update)
    except BaseException as exception:
        logger.exception(exception)


@app.post('/api/telegram/webhook/{token}')
async def webhook_handler(update: types.Update, token: str):
    assert token == settings.BOT_TOKEN, (status.HTTP_418_IM_A_TEAPOT, ':(')
    return await handle_update(update)
