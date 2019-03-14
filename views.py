# -*- coding: utf-8 -*-

"""Views for 'avito_api' application."""
import json
from aiohttp import web
from models import (
    select_all_companies,
    select_company,
    RecordNotFound,
    insert_company,
    select_all_employees,
    insert_employee,
    employee_to_company,
    insert_item,
    item_to_employee,
)


async def get_all_companies(request):
    """Return list of all companies."""
    async with request.app['db'].acquire() as conn:
        companies_list = await select_all_companies(conn)
        return web.Response(text=json.dumps(companies_list))


async def get_company(request):
    """Return one company by ID."""
    async with request.app['db'].acquire() as conn:
        company_id = request.match_info.get('company_id')
        try:
            select_result = await select_company(conn, company_id)
        except RecordNotFound as ex:
            raise web.HTTPNotFound(text=str(ex))
        return web.Response(text=json.dumps(select_result))


async def add_company(request):
    """Add company by name. Return company."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        company_name = post_body['company_name']
        new_company = await insert_company(conn, company_name)
        return web.Response(text=json.dumps(new_company))


async def get_all_employees(request):
    """Return all employees from DB."""
    async with request.app['db'].acquire() as conn:
        employees_list = await select_all_employees(conn)
        return web.Response(text=json.dumps(employees_list))


async def add_employee(request):
    """Add new employee by name. Return new employee."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        employee_name = post_body['employee_name']
        new_employee = await insert_employee(conn, employee_name)
        return web.Response(text=json.dumps(new_employee))


async def assign_employee(request):
    """Assign employee to company. Return assigned employee."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        employee_id = post_body['employee_id']
        company_id = post_body['company_id']
        new_assignee = await employee_to_company(conn, employee_id, company_id)
        return web.Response(text=json.dumps(new_assignee))


async def add_item(request):
    """Add new item to company goods. Return item."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        item_name = post_body['item_name']
        company_id = post_body['company_id']
        new_item = await insert_item(conn, item_name, company_id)
        return web.Response(text=json.dumps(new_item))


async def assign_item(request):
    """Assign item to employee. Return item."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        item_id = post_body['item_id']
        employee_id = post_body['employee_id']
        new_assignee = await item_to_employee(conn, item_id, employee_id)
        return web.Response(text=json.dumps(new_assignee))
