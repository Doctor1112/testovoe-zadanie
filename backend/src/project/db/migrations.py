import contextlib
from unittest.mock import patch

from aerich import Command
from loguru import logger

from project.db.config import config
from project.settings import settings

MIGRATIONS_DIR = settings.PROJECT_DIR.joinpath('migrations')


async def run_migration():
    command = Command(tortoise_config=config, location=MIGRATIONS_DIR)
    logger.info('Run db migration...')
    with contextlib.suppress(FileExistsError):
        await command.init_db(safe=True)
    await command.init()
    with patch('click.prompt', return_value=True):
        await command.migrate()
    await command.upgrade(run_in_transaction=True)
    logger.info('Db successfully upgraded')
