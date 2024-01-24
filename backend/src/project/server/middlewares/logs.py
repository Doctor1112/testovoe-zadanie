from fastapi import HTTPException
from fastapi.requests import Request
from loguru import logger
from starlette.responses import JSONResponse

from project.server import app


def request_info(request: Request) -> str:
    return f'{request.url.path} {request.method}'


@app.middleware('http')
async def logging_query(request: Request, call_next):
    logger.info(f'request {request_info(request)}')
    response = await call_next(request)
    logger.info(f'response {request_info(request)} {response.status_code}')
    return response


@app.exception_handler(HTTPException)
async def logging_error(request: Request, e: HTTPException):
    logger.info(f'error {request_info(request)} {e.detail}')
    return JSONResponse(dict(detail=e.detail), status_code=e.status_code)


@app.exception_handler(Exception)
async def logging_exception(request: Request, e: Exception):
    detail = f'{type(e).__name__}: {e}'
    logger.info(f'error {request_info(request)} {detail}')
    logger.exception(e)
    return JSONResponse(dict(detail=detail), status_code=500)
