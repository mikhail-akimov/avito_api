from aiohttp import web
from models import goods, employee, company, select_company, RecordNotFound, insert_company, insert_employee, employee_to_company, insert_item, item_to_employee
import json


async def handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = 'Hello, ' + name
    return web.Response(text=text)


async def get_all_companies(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(company.select())
        records = await cursor.fetchall()
        companies = [dict(q) for q in records]
        return web.Response(text=str(companies))


async def get_company(request):
    async with request.app['db'].acquire() as conn:
        company_id = request.match_info.get('company_id')
        try:
            result = await select_company(conn, company_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return web.Response(text=json.dumps(result))


async def add_company(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        company_name = data['company_name']
        new_company = await insert_company(conn, company_name)
        return web.Response(text=json.dumps(new_company))


async def get_all_employees(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(employee.select())
        records = await cursor.fetchall()
        employees = [dict(emp) for emp in records]
        return web.Response(text=str(employees))


async def add_employee(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        employee_name = data['employee_name']
        new_employee = await insert_employee(conn, employee_name)
        return web.Response(text=json.dumps(new_employee))


async def assign_employee(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        employee_id = data['employee_id']
        company_id = data['company_id']
        new_assignee = await employee_to_company(conn, employee_id, company_id)
        return web.Response(text=json.dumps(new_assignee))


async def add_item(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        item_name = data['item_name']
        company_id = data['company_id']
        new_item = await insert_item(conn, item_name, company_id)
        return web.Response(text=json.dumps(new_item))


async def assign_item(request):
    async with request.app['db'].acquire() as conn:
        data = await request.json()
        item_id = data['item_id']
        employee_id = data['employee_id']
        new_assignee = await item_to_employee(conn, item_id, employee_id)
        return web.Response(text=json.dumps(new_assignee))
