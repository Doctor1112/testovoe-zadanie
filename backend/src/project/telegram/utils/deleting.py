import contextlib
import typing

from aiogram import types, Bot
from aiogram.exceptions import TelegramAPIError

from project.db.models import User

TRASH_KEY = 'messages_to_delete'

Message: typing.TypeAlias = types.Message | types.MessageId


class TrashManager:
    """
    This is a context manager that's created to handle the user's trash context.
    It cleans up the operations related to the trash context of a user,
    initializing it if it's not already present,
    and saving the user context when the operations are done.
    """

    def __init__(self, user: User):
        self.user = user

    async def __aenter__(self):
        if TRASH_KEY not in self.user.context:
            self.user.context[TRASH_KEY] = []
            await self.user.save()
        return self.user.context[TRASH_KEY]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.user.save()


def message_to_ids(user: User, message: Message):
    return [
        message.chat.id if isinstance(message, types.Message) else user.id,
        message.message_id,
    ]


async def delete_pending_messages(user: User):
    bot = Bot.get_current()
    async with TrashManager(user) as trash:
        for chat_id, message_id in trash:
            with contextlib.suppress(TelegramAPIError):
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
        trash.clear()


async def schedule_messages_deletion(user: User, *messages: Message):
    async with TrashManager(user) as trash:
        trash.extend([message_to_ids(user, message) for message in messages])


async def reschedule_message_deletion(user: User, message: Message, *, old_message: Message):
    async with TrashManager(user) as trash:
        index = trash.index(message_to_ids(user, old_message))
        trash[index] = message_to_ids(user, message)


async def schedule_message_deletion(user: User, message: Message):
    async with TrashManager(user) as trash:
        trash.append(message_to_ids(user, message))


async def is_scheduled_to_deletion(user: User, message: Message) -> bool:
    async with TrashManager(user) as trash:
        return message_to_ids(user, message) in trash
