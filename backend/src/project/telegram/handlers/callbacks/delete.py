from aiogram import types
from project.telegram.events.delete import DeleteEvent

from project.telegram import dp
from project.telegram.utils.handler import handler


@dp.callback_query(DeleteEvent.filter())
@handler
async def delete(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()
