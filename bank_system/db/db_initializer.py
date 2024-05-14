import db_manager
import queries as q


def create_tables(cursor):
    cursor.execute(q.CREATE_TABLE_USER)
    cursor.execute(q.CREATE_TABLE_ACCOUNT)
    cursor.execute(q.CREATE_TABLE_TRANSACTION)


if __name__ == "__main__":
    with db_manager.DBManager() as db:
        create_tables(db.cursor)


