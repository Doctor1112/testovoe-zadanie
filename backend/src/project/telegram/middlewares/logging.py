from typing import Callable

from aiogram import BaseMiddleware, types
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, update: types.Update, data: dict):
        logger.debug(update.json())
        return await handler(update, data)
