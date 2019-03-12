from aiohttp import web


async def handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = 'Hello, ' + name
    return web.Response(text=text)


async def get_all_companies(request):
    text = 'All company list! {0}'.format(request)
    return web.Response(text=text)


async def get_company(request):
    company_id = request.match_info.get('company_id')
    text = 'One company data for company - {0}!'.format(company_id)
    return web.Response(text=text)


async def add_company(request):
    company_name = request.match_info.get('company_name')
    text = 'Request to add company - {0} - processed!'.format(company_name)
    return web.Response(text=text)


async def add_employee(request):
    text = 'Request to add employee processed! {0}'.format(request)
    return web.Response(text=text)


async def assign_employee(request):
    text = 'Request to assign employee processed! {0}'.format(request)
    return web.Response(text=text)


async def add_item(request):
    text = 'Request to add item processed! {0}'.format(request)
    return web.Response(text=text)


async def assign_item(request):
    text = 'Request to assign item processed! {0}'.format(request)
    return web.Response(text=text)
