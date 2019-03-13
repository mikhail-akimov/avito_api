from sqlalchemy import (MetaData, Table, Column, Integer, String, ForeignKey)
import aiopg.sa

__all__ = ['company', 'employee', 'goods']

meta = MetaData()

company = Table(
    'company', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False)
)

employee = Table(
    'employee', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('company', Integer, ForeignKey('company.id', ondelete='CASCADE')),
    Column('phone', String(20))
)

goods = Table(
    'goods', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('company', Integer, ForeignKey('company.id', ondelete='CASCADE'), nullable=False),
    Column('employee', Integer, ForeignKey('employee.id', ondelete='CASCADE'))
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
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
    app['db'].close()
    await app['db'].wait_closed()


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def select_company(conn, company_id):
    result = await conn.execute(company.select().where(company.c.id == company_id))
    first_row = await result.first()
    result = {'id': first_row[0],
              'name': first_row[1]
              }
    if not result:
        msg = 'Company with id: {0} does not exists!'
        raise RecordNotFound(msg.format(company_id))
    return result


async def insert_company(conn, company_name):
    try:
        result = await conn.execute(company.insert({'name': company_name}))
        if result.returns_rows:
            result = await conn.execute(company.select().where(company.c.name == company_name))
            records = await result.fetchall()
            result = [dict(comp) for comp in records][-1]
    except Exception as e:
        result = 'Error! {}'.format(e)
    return result


async def insert_employee(conn, employee_name):
    try:
        result = await conn.execute(
            employee.insert({'name': employee_name}))
        if result.returns_rows:
            result = await conn.execute(employee.select().where(employee.c.name == employee_name))
            records = await result.fetchall()
            emp = [dict(emp) for emp in records][-1]
            result = {'id': emp['id'],
                      'name': emp['name']
                      }
    except Exception as e:
        result = 'Error! {}'.format(e)
    return result


async def employee_to_company(conn, employee_id, company_id):
    try:
        new_assignee = await conn.execute(
            employee.update().where(employee.c.id == employee_id).values(company=company_id))
        result = await conn.execute(employee.select().where(employee.c.id == employee_id))
        result = [dict(emp) for emp in result][0]
    except Exception as e:
        result = 'Error! {}'.format(e)
    return result


async def insert_item(conn, item_name, company_id):
    try:
        result = await conn.execute(goods.insert({'name': item_name, 'company': company_id}))
        if result.returns_rows:
            result = await conn.execute(goods.select().where(goods.c.name == item_name))
            records = await result.fetchall()
            itm = [dict(itm) for itm in records][-1]
            result = {'id': itm['id'],
                      'name': itm['name'],
                      'company': itm['company']
                      }
    except Exception as e:
        result = 'Error! {}'.format(e)
    return result


async def item_to_employee(conn, item_id, employee_id):
    try:
        new_assignee = await conn.execute(
            goods.update().where(goods.c.id == item_id).values(employee=employee_id))
        result = await conn.execute(goods.select().where(goods.c.id == item_id))
        result = [dict(emp) for emp in result][0]
    except Exception as e:
        result = 'Error! {}'.format(e)
    return result
