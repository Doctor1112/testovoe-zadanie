from starlette.requests import Request

from project.server import app
from project.settings import settings


@app.middleware('http')
async def subdomain_cors_middleware(request: Request, call_next):
    response = await call_next(request)
    origin = request.headers.get('origin')
    if origin and origin.endswith(settings.DOMAIN):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, ' \
                                                           'Authorization, X-Requested-With'
    return response
