from typing import Callable

from aiogram import BaseMiddleware
from aiogram import types

from project.db.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: types.TelegramObject, data: dict):
        user = await User.get_current()
        data['user'] = user
        return await handler(event, data)
