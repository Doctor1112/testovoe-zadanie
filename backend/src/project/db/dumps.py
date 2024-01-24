import subprocess
from datetime import datetime

from loguru import logger

from project.definitions import DUMPS_DIR
from project.settings import settings


def create_pg_dump():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dump_file_path = DUMPS_DIR.joinpath(f'{settings.POSTGRES_DB}_{timestamp}.sql')
    command = f'pg_dump -h db -U {settings.POSTGRES_USER} -d {settings.POSTGRES_DB} -f {dump_file_path} -w'

    logger.debug(f"Start pg_dump")
    subprocess.run(command, check=True, shell=True)
    logger.debug(f"Database dump successfully created at {dump_file_path}")
