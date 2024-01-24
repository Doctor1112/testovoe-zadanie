from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from project.telegram import dp
from project.telegram.utils.answer import answer
from project.telegram.utils.handler import handler


@dp.message(Command('start'))
@handler
async def start(message: types.Message, state: FSMContext):
    await answer(chat_id=message.chat.id, text='Hello, world!')
