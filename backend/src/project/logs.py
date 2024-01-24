import logging
import logging.handlers
import re
import sys

from loguru import logger

from project.definitions import LOGS_DIR
from project.settings import settings

log_file = (
    "{time:DD-MM-YYYY}/log.log"
)

logger_format = (
    '<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green>'
    '<red> [ <level>{level}</level> ] </red>'
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> → {message}'
)

logger_file_format = (
    '{time:YYYY-MM-DD HH:mm:ss.SS}'
    ' [ <level>{level}</level> ] '
    '{name}:{function}:{line} → {message}'
)

loggers_blacklist = [
    'pyrogram.session',
    'pyrogram.connection',
]


def hide_secrets(record: dict):
    record['message'] = record['message'].replace(settings.BOT_TOKEN, '[TG_BOT_TOKEN]')


def whitelist_filter(message: str | dict) -> bool:
    if isinstance(message, dict):
        message = message.get("name", "")
    if any(re.match(regex, message) for regex in loggers_blacklist):
        return False
    return True


def configure_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # configure loguru logging
    logger.remove(0)
    logger.add(
        sink=sys.stdout,
        filter=whitelist_filter,
        level=log_level,
        format=logger_format,
        backtrace=False,
        colorize=True,
    )
    logger.add(
        sink=LOGS_DIR.joinpath(log_file),
        rotation="1 MB",
        retention="2 weeks",
        compression="zip",
        filter=whitelist_filter,
        level=logging.DEBUG,
        format=logger_file_format,
        backtrace=False,
        colorize=False,
    )
    logger.configure(patcher=hide_secrets)

    # handle all default logging
    logging.basicConfig(handlers=[InterceptHandler()], level=log_level, force=True)

    # configure default logging
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)


# Intercept standard logging messages
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 0
        skip = True
        while (is_log_frame := frame.f_code.co_filename == logging.__file__) or skip:
            if skip and is_log_frame:
                skip = False
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
