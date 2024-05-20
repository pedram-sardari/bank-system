from . import db_manager
from . import db_queries as q


def create_tables(cursor):
    print(__name__, "Creating tables..." * 1)
    cursor.execute(q.CREATE_TABLE_USER)
    cursor.execute(q.CREATE_TABLE_ACCOUNT)
    cursor.execute(q.CREATE_TABLE_TRANSACTION)
    cursor.execute(q.CREATE_TABLE_TRANSACTION_LOG)


with db_manager.DBManager() as cur:
    create_tables(cur)
