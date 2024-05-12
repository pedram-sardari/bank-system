import psycopg2
from psycopg2 import extras
from db_config import load_db_confing


class DBManager:
    def __init__(self):
        self.db_config = load_db_confing()
        self.connection = None
        self.cursor = None

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def __enter__(self):
        try:
            print(self.db_config)
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.DatabaseError:
            print("\033[90mDatabaseError\033[0m")
        else:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_tb or exc_val or exc_tb:
                self.rollback()
            else:
                self.commit()
            self.connection.close()


if __name__ == '__main__':
    with DBManager() as db:
        db.cursor.execute("CREATE TABLE f (a int);")
