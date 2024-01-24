from contextlib import contextmanager
from typing import Type

from fastapi import HTTPException
from fastapi import status


@contextmanager
def server_exceptions(*exceptions: Type[BaseException], status_code: status = 400, detail: str = None):
    # noinspection PyBroadException
    try:
        yield
    except exceptions as exception:
        if detail is None:
            detail = f'{exception.__class__.__name__}: {exception}'
        raise HTTPException(status_code=status_code, detail=detail)
