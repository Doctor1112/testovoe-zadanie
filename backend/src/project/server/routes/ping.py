from project.server import app


@app.get('/api/ping')
async def ping():
    return {'hello': 'there!'}
