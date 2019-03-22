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
from validations import (
    validate,
    get_all_companies_output,
    exceptions,
    get_all_employees_output,
    get_one_company_output,
    add_company_input,
    add_company_output,
    add_employee_input,
    add_employee_output,
    assign_employee_input,
    assign_employee_output,
    add_item_input,
    add_item_output,
    assign_item_input,
    assign_item_output,
)


async def get_all_companies(request):
    """Return list of all companies."""
    async with request.app['db'].acquire() as conn:
        companies_list = await select_all_companies(conn)
        try:
            validate(instance=companies_list, schema=get_all_companies_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(companies_list))


async def get_company(request):
    """Return one company by ID."""
    async with request.app['db'].acquire() as conn:
        company_id = request.match_info.get('company_id')
        try:
            select_result = await select_company(conn, company_id)
        except RecordNotFound as ex:
            raise web.HTTPNotFound(text=str(ex))
        try:
            validate(instance=select_result, schema=get_one_company_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(select_result))


async def add_company(request):
    """Add company by name. Return company."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        try:
            validate(instance=post_body, schema=add_company_input)
        except exceptions.ValidationError as ex:
            error_message = 'Sorry, you send invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        else:
            new_company = await insert_company(conn, post_body['company_name'])
        try:
            validate(instance=new_company, schema=add_company_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(new_company))


async def get_all_employees(request):
    """Return all employees from DB."""
    async with request.app['db'].acquire() as conn:
        employees_list = await select_all_employees(conn)
        try:
            validate(instance=employees_list, schema=get_all_employees_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(employees_list))


async def add_employee(request):
    """Add new employee by name. Return new employee."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        try:
            validate(instance=post_body, schema=add_employee_input)
        except exceptions.ValidationError as ex:
            error_message = 'Sorry, you send invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        new_employee = await insert_employee(conn, post_body['employee_name'])
        try:
            validate(instance=new_employee, schema=add_employee_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(new_employee))


async def assign_employee(request):
    """Assign employee to company. Returns assigned 'employee'."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        try:
            validate(instance=post_body, schema=assign_employee_input)
        except exceptions.ValidationError as ex:
            error_message = 'Sorry, you send invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        new_assignee = await employee_to_company(
            conn,
            post_body['employee_id'],
            post_body['company_id'],
        )
        try:
            validate(instance=new_assignee, schema=assign_employee_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(new_assignee))


async def add_item(request):
    """Add new item to company goods. Returns 'item'."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        try:
            validate(instance=post_body, schema=add_item_input)
        except exceptions.ValidationError as ex:
            error_message = 'Sorry, you send invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        new_item = await insert_item(
            conn,
            post_body['item_name'],
            post_body['company_id'],
        )
        try:
            validate(instance=new_item, schema=add_item_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(new_item))


async def assign_item(request):
    """Assign item to employee. Returns assigned 'item'."""
    async with request.app['db'].acquire() as conn:
        post_body = await request.json()
        try:
            validate(instance=post_body, schema=assign_item_input)
        except exceptions.ValidationError as ex:
            error_message = 'Sorry, you send invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        new_assignee = await item_to_employee(
            conn,
            post_body['item_id'],
            post_body['employee_id'],
        )
        try:
            validate(instance=new_assignee, schema=assign_item_output)
        except exceptions.ValidationError as ex:
            error_message = 'Server returns invalid data...\n{0}'.format(ex)
            return web.Response(text=error_message)
        return web.Response(text=json.dumps(new_assignee))
