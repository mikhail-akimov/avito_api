# -*- coding: utf-8 -*-

"""Models for 'avito_api' application."""
from sqlalchemy import (MetaData, Table, Column, Integer, String, ForeignKey)
from aiopg.sa import create_engine


meta = MetaData()

company = Table(
    'company',
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
)

employee = Table(
    'employee',
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('company', Integer, ForeignKey('company.id', ondelete='CASCADE')),
    Column('phone', String(20)),
)

goods = Table(
    'goods',
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column(
        'company',
        Integer,
        ForeignKey('company.id', ondelete='CASCADE'),
        nullable=False,
    ),
    Column('employee', Integer, ForeignKey('employee.id', ondelete='CASCADE')),
)


async def init_pg(app):
    """Init pg database engine."""
    conf = app['config']['postgres']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    """Close PostgreSQL engine."""
    app['db'].close()
    await app['db'].wait_closed()


class RecordNotFound(Exception):
    """Requested record in database was not found."""


async def select_all_companies(conn):
    """Select from db list of all companies."""
    cursor = await conn.execute(company.select())
    records = await cursor.fetchall()
    companies = [dict(comp) for comp in records]
    return companies


async def select_company(conn, company_id):
    """Select from db one company by unique id."""
    select_comp = await conn.execute(
        company.select().where(company.c.id == company_id)
    )
    first_row = await select_comp.first()
    if first_row:
        comp = {'id': first_row[0],
                'name': first_row[1],
                }
    else:
        msg = 'Company with id: {0} does not exists!'
        raise RecordNotFound(msg.format(company_id))
    return comp


async def insert_company(conn, company_name):
    """Insert a new company to db by name."""
    try:
        insert_comp = await conn.execute(
            company.insert({'name': company_name})
        )
        new_company = insert_comp
        if insert_comp.returns_rows:
            select_comp = await conn.execute(
                company.select().where(company.c.name == company_name)
            )
            records = await select_comp.fetchall()
            new_company = [dict(comp) for comp in records][-1]
    except Exception as ex:
        new_company = 'Error! {0}'.format(ex)
    return new_company


async def select_all_employees(conn):
    """Select from database list of all employees."""
    cursor = await conn.execute(employee.select())
    records = await cursor.fetchall()
    employees = [dict(emp) for emp in records]
    return employees


async def insert_employee(conn, employee_name):
    """Insert a new employee to db by name."""
    try:
        insert_emp = await conn.execute(
            employee.insert({'name': employee_name})
        )
        new_employee = insert_emp
        if insert_emp.returns_rows:
            select_emp = await conn.execute(
                employee.select().where(employee.c.name == employee_name)
            )
            records = await select_emp.fetchall()
            emp = [dict(emp) for emp in records][-1]
            new_employee = {'id': emp['id'],
                            'name': emp['name'],
                            }
    except Exception as ex:
        new_employee = 'Error! {0}'.format(ex)
    return new_employee


async def employee_to_company(conn, employee_id, company_id):
    """Assign existing employee to existing company."""
    try:
        assign_employee = await conn.execute(
            employee.update().where(
                employee.c.id == employee_id
            ).values(company=company_id)
        )
        select_emp = await conn.execute(
            employee.select().where(employee.c.id == employee_id)
        )
        new_assignee = [dict(emp) for emp in select_emp][0]
    except Exception as ex:
        new_assignee = 'Error! {0}'.format(ex)
    return new_assignee


async def insert_item(conn, item_name, company_id):
    """Insert a new item to db by name and company_id."""
    try:
        insert = await conn.execute(
            goods.insert({'name': item_name, 'company': company_id})
        )
        new_item = insert
        if insert.returns_rows:
            select_item = await conn.execute(
                goods.select().where(goods.c.name == item_name)
            )
            records = await select_item.fetchall()
            itm = [dict(itm) for itm in records][-1]
            new_item = {'id': itm['id'],
                        'name': itm['name'],
                        'company': itm['company'],
                        }
    except Exception as ex:
        new_item = 'Error! {0}'.format(ex)
    return new_item


async def item_to_employee(conn, item_id, employee_id):
    """Assign existing item to existing employee."""
    try:
        new_assignee = await conn.execute(
            goods.update().where(
                goods.c.id == item_id
            ).values(employee=employee_id)
        )
        select_item = await conn.execute(
            goods.select().where(goods.c.id == item_id)
        )
        assigned_item = [dict(emp) for emp in select_item][0]
    except Exception as ex:
        assigned_item = 'Error! {0}'.format(ex)
    return assigned_item
