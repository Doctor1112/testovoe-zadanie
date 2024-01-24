import mimetypes
from pathlib import Path

from aiogram import types
from aiogram.utils.i18n import get_i18n

from project.definitions import LOCALES_DIR


def getmedia(filename: str, *, locale: str = None) -> types.InputMedia | None:
    locale = locale or get_i18n().default_locale
    media_dir = LOCALES_DIR.joinpath(locale).joinpath('media')
    media_file = media_dir.joinpath(filename)
    if not media_file.is_file():
        return None
    media_type = guess_media_type(media_file)
    return media_type(media=types.FSInputFile(media_file))


def guess_media_type(file: Path) -> type[types.InputMedia]:
    default_media_type = types.InputMediaDocument
    mimetype, *_ = mimetypes.guess_type(file)
    if mimetype is None:
        return default_media_type
    discrete_type = mimetype[:mimetype.index('/')]
    return {  # TODO: expand with other types
        'image': types.InputMediaPhoto,
        'video': types.InputMediaVideo,
    }.get(discrete_type, default_media_type)
