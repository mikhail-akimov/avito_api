# -*- coding: utf-8 -*-

import asyncio
from aiohttp import web
from config.settings import config
from routes import setup_routes
from models import init_pg, close_pg
from init_db import container_start


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
setup_routes(app)
app['config'] = config

if __name__ == '__main__':
    container_start()
    web.run_app(app)
