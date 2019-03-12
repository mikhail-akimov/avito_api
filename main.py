import asyncio
from aiohttp import web
from config.settings import config
from routes import setup_routes

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
setup_routes(app)
app['config'] = config

web.run_app(app)
