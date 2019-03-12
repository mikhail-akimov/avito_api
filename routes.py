from views import handler, get_all_companies, get_company, add_company, \
    add_employee, assign_employee, add_item, assign_item


def setup_routes(app):
    # app.router.add_route('GET', '/', handler)
    # app.router.add_route('GET', '/{name}', handler)
    app.router.add_route('GET', '/company', get_all_companies)
    app.router.add_route('GET', '/company/{company_id}', get_company)
    app.router.add_route('POST', '/company/add', add_company)
    app.router.add_route('POST', '/employee/add', add_employee)
    app.router.add_route('PUT', '/employee/assign', assign_employee)
    app.router.add_route('POST', '/company/goods/add', add_item)
    app.router.add_route('PUT', '/company/goods/assign', assign_item)
