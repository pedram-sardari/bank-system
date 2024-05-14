import hashlib
from .. import messages as m
from ..db import queries as q, db_manager


class User:
    def __init__(self, username, password):
        self.username = username  # TODO: unique username
        self.password = password

    @staticmethod
    def hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = User.hash_password(new_password)

    def register(self, cursor):
        """TODO: insert query /
         TOD0: error handling -> long-string / duplicated username"""
        cursor.execute(q.REGISTER_NEW_USER, (self.username, self.password))

    @staticmethod
    def login(username, password, cursor):
        # TODO: return value? user_obj / tuple
        cursor.execute(q.LOGIN_USER, (username, User.hash_password(password)))
        user_record = cursor.fetchone()
        if user_record:
            return user_record
        raise ValueError(m.Messages.INVALID_USERNAME_OR_PASSWORD_ERROR)


if __name__ == '__main__':
    user = User("pedi", "1234")
    with db_manager.DBManager() as db:
        user.register(db.cursor)
        # print(User.login("pedi", "1234", db.cursor))
        # print(User.login("edi", "1234", db.cursor))
