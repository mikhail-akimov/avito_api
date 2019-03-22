import pytest
from aiohttp import web
from views import (
    get_all_employees,
    add_employee
)
from config.settings import config
from routes import setup_routes
from models import init_pg, close_pg


def create_app(loop):
    app = web.Application(loop=loop)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    setup_routes(app)
    app['config'] = config
    app.router.add_route('GET', '/employee', get_all_employees)
    app.router.add_route('POST', '/employee/add', add_employee)
    return app


async def test_get_all_employees(test_client):
    client = await test_client(create_app)
    correct_resp = await client.get('/employee')
    assert correct_resp.status == 200
    incorrect_resp = await client.get('/employe')
    assert incorrect_resp.status == 404


async def test_add_employee(test_client):
    client = await test_client(create_app)
    correct_resp = await client.post('/employee/add', data='{"employee_name": "Test_employee"}')
    text = await correct_resp.text()
    assert '"name": "Test_employee"' in text
    incorrect_resp = await client.post('/employee/add', data='{"employee": "Test_employee"}')
    text = await incorrect_resp.text()
    assert 'Failed validating' in text
    incorrect_resp = await client.post('/employee/ad', data='{"employee_name": "Test_employee"}')
    assert incorrect_resp.status == 404
    incorrect_resp = await client.post('/employee/add', data='')
    assert incorrect_resp.status == 500
