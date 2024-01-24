from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from project.server import app


def create_response(status_code: int = 400, detail: str = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(dict(detail=detail)),
    )


@app.exception_handler(AssertionError)
async def assertions_to_json(_, exc: AssertionError):
    if not exc.args:
        return create_response(400)
    match exc.args[0]:
        case [int(status_code), str(detail)]:
            return create_response(
                status_code=status_code,
                detail=detail,
            )
        case [str(detail), int(status_code)]:
            return create_response(
                status_code=status_code,
                detail=detail,
            )
        case int(status_code):
            return create_response(
                status_code=status_code,
            )
        case str(detail):
            return create_response(
                status_code=400,
                detail=detail,
            )
        case _:
            return create_response(
                status_code=500,
                detail='Invalid server assertion',
            )
