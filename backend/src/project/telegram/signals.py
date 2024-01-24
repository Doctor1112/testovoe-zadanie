from aiogram import Bot
from loguru import logger

from project.settings import settings
from project.utils.wait_for_it import wait_for_it


async def on_startup():
    bot = Bot.get_current()
    timeout = 15
    external_url = f'https://{settings.DOMAIN}'
    logger.info(f'Wait for access to {external_url} for {timeout} seconds...')
    wait_for_it(external_url, timeout=timeout)
    logger.info(f'External url is reachable!')
    await bot.delete_webhook()
    await bot.set_webhook(f'{external_url}/api/telegram/webhook/{settings.BOT_TOKEN}')


async def on_shutdown():
    bot = Bot.get_current()
    await bot.delete_webhook()
