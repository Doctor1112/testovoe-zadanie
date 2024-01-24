import subprocess

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware, I18n

from project.definitions import LOCALES_DIR

LOCALES_DOMAIN = 'texts'


class DBI18nMiddleware(I18nMiddleware):
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    async def get_locale(self, event: TelegramObject, data: dict) -> str:
        return data['user'].language

    def __init__(self):
        subprocess.run(f'pybabel compile -f -d {LOCALES_DIR} -D {LOCALES_DOMAIN}'.split())
        i18n = I18n(path=LOCALES_DIR, default_locale='ru', domain=LOCALES_DOMAIN)
        super().__init__(i18n, middleware_key='i18n')
        I18n.set_current(i18n)
