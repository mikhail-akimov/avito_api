from sqlalchemy import create_engine, MetaData

from models import company, employee, goods
from config.settings import BASE_DIR, get_config, config_path


DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host='postgres', port=5432
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG_PATH = BASE_DIR / 'config' / 'api.yaml'
USER_CONFIG = get_config(config_path)
USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_engine(USER_DB_URL)
#
# TEST_CONFIG_PATH = BASE_DIR / 'config' / 'polls_test.yaml'
# TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
# TEST_DB_URL = DSN.format(**TEST_CONFIG['postgres'])
# test_engine = create_engine(TEST_DB_URL)


def check_db(engine=user_engine):
    conn = engine.connect()
    if conn:
        return True
    else:
        return False


def setup_db(config):
    db_name = config['database']
    db_user = config['user']
    db_pass = config['password']

    conn = admin_engine.connect()
    conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
    conn.execute('DROP ROLE IF EXISTS %s' % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute('CREATE DATABASE %s ENCODING "UTF8"' % db_name)
    conn.execute('GRANT ALL PRIVILEGES ON DATABASE %s TO %s' %
                 (db_name, db_user))
    conn.close()


def teardown_db(config):

    db_name = config['database']
    db_user = config['user']

    conn = admin_engine.connect()
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
    conn.execute('DROP ROLE IF EXISTS %s' % db_user)
    conn.close()


def create_tables(engine=user_engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[company, employee, goods])


def drop_tables(engine=user_engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[company, employee, goods])


def sample_data(engine=user_engine):
    conn = engine.connect()
    conn.execute(company.insert(), [
        {'name': 'Testompany'},
        {'name': 'Another_test_company'}
    ])
    conn.execute(employee.insert(), [
        {'name': 'Vasiliy', 'company': 1, 'phone': '+79991234567'},
        {'name': 'Павел', 'company': None, 'phone': None}
    ])
    conn.execute(goods.insert(), [
        {'name': 'Bike', 'employee': 1, 'company': 1},
        {'name': 'Car', 'employee': None, 'company': 2}
    ])
    conn.close()


def container_start():
    try:
        check_db(engine=user_engine)
    except Exception:
        setup_db(USER_CONFIG['postgres'])
        create_tables(engine=user_engine)
        sample_data(engine=user_engine)
        # drop_tables()
        # teardown_db(config)
    return True


if __name__ == '__main__':
    if not check_db(engine=user_engine):
        setup_db(USER_CONFIG['postgres'])
        create_tables(engine=user_engine)
        sample_data(engine=user_engine)
        # drop_tables()
        # teardown_db(config)
    else:
        print('No need to init!')
