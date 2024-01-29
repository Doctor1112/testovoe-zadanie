from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from project import settings

from project.telegram import dp
from project.telegram.utils.answer import answer
from project.telegram.utils.handler import handler
from aiogram.types.web_app_info import WebAppInfo
from project.db.models import User
from aiogram import types


class RegistrationStates(StatesGroup):
    GET_NAME = State()
    GET_AGE = State()


@dp.message(Command("signup"))
@handler
async def start(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationStates.GET_NAME)
    await answer(chat_id=message.chat.id, text="Как тебя зовут?")


@dp.message(RegistrationStates.GET_NAME)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationStates.GET_AGE)

    await answer(
        chat_id=message.chat.id,
        text=f"Приятно познакомиться, {message.text}! Сколько тебе лет?",
    )


@dp.message(RegistrationStates.GET_AGE)
async def process_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    age = message.text
    user = await User.get_current()
    try:
        age = int(age)
    except:
        await answer(
        chat_id=message.chat.id,
        text="Введи корректный возраст",
    )
        return
    user.age = age
    user.first_name = data["name"]
    await user.save(update_fields=("age", "first_name"))
    user_cnt = await User.all().count()
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Открыть веб страницу",
                    web_app=WebAppInfo(
                        url=f"https://{settings.settings.DOMAIN}/?name={data['name']}&age={age}&user_cnt={user_cnt}",
                    ),
                )
            ]
        ]
    )
    await state.clear()
    await answer(
        chat_id=message.chat.id,
        text="Вы успешно зарегистрированы!",
        reply_markup=markup,
    )