import asyncio
from aiohttp import web

loop = asyncio.get_event_loop()


async def handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = 'Hello, ' + name
    return web.Response(text=text)


app = web.Application(loop=loop)
app.router.add_route('GET', '/', handler)
app.router.add_route('GET', '/{name}', handler)
# app.router.add_route('GET', '/company',)
# app.router.add_route('GET', '/company/{company_id}',)
# app.router.add_route('POST', '/company/add',)
# app.router.add_route('POST', '/employee/add')
# app.router.add_route('PUT', '/employee/assign')
# app.router.add_route('POST', '/company/goods/add')
# app.router.add_route('PUT', '/company/goods/assign')

web.run_app(app)
