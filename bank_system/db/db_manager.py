import psycopg2
from psycopg2 import extras
from .db_config import load_db_confing


class DBManager:
    def __init__(self, cursor_type='DictCursor'):
        """
        :param cursor_type: 'DictCursor' or 'RealDictCursor'
        """
        self.db_config = load_db_confing()
        self.connection = self.create_new_connection()
        self.cursor_type = cursor_type
        self.cursor = None

    def create_new_connection(self):
        try:
            connection = psycopg2.connect(**self.db_config)
        except psycopg2.DatabaseError:
            print("\033[90mDatabaseError\033[0m")
            return None
        else:
            return connection

    def create_new_cursor(self):
        if self.cursor_type == 'RealDictCursor':
            cursor_factory = psycopg2.extras.RealDictCursor
        else:
            cursor_factory = psycopg2.extras.DictCursor
        return self.connection.cursor(cursor_factory=cursor_factory)

    def change_cursor_type(self, new_cursor_type):
        """
        :param new_cursor_type: 'DictCursor' or 'RealDictCursor'
        """
        self.cursor_type = new_cursor_type

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute_query(self, query: str, params: tuple):
        if self.cursor:
            self.cursor(query, params)
        else:
            raise ValueError("\033[91mThere's no cursor object in this database manager object!")

    def fetch_one(self):
        return self.cursor.fetchone()

    def fetch_all(self):
        return self.cursor.fetchall()

    def __enter__(self):
        self.cursor = self.create_new_cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            if exc_tb or exc_val or exc_tb:
                self.rollback()
            else:
                self.commit()

    def __del__(self):
        print('Closing connection ...')
        self.connection.close()


if __name__ == '__main__':
    # cursor_type='RealDictCursor'
    db_manager = DBManager()
    with db_manager as cursor:
        cursor.execute("CREATE TABLE f (a INT);")
        cursor.execute("INSERT INTO f (a) VALUES (50)")
        # db_manager.commit()
        cursor.execute("SELECT * FROM f")

        cursor.execute("UPDATE users SET username='maman' WHERE username='pedi'")
        cursor.execute("INSERT INTO users (username, password) VALUES ('hasan', '2341341')")
        cursor.execute("SELECT * FROM users")
        # print(cursor.fetchall())
        print(cursor.fetchone())
        print(cursor.fetchone())
        print(cursor.fetchone())
        print(cursor.fetchone())
    print(db_manager.cursor)