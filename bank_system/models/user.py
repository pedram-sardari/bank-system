import hashlib
from typing import Self
from .. import messages as m
from .. import constance as c
from ..db import queries as q, db_manager


class User:
    def __init__(self, username, password, user_id=None):
        self.user_id = user_id
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

    def validate_username(self, cursor):
        cursor.execute(q.USERNAME_EXISTENCE, (self.username,))
        user_id = cursor.fetchone()
        if user_id:
            raise ValueError(m.Messages.USERNAME_ALREADY_EXISTS_ERROR.format(self.username))
        if len(self.username) > c.MAXIMUM_USERNAME_LENGTH:
            raise ValueError()  # TODO: proper message

    def register(self, cursor):
        """TODO: insert query /
         TOD0: error handling -> long-string / duplicated username"""
        self.validate_username(cursor)
        cursor.execute(q.REGISTER_NEW_USER, (self.username, self.password))

    @classmethod
    def login(cls, username, password, cursor) -> Self:
        hashed_password = User.hash_password(password)
        cursor.execute(q.LOGIN_USER, (username, hashed_password))
        user_record = cursor.fetchone()
        if user_record:
            return cls(**user_record)
        raise ValueError(m.Messages.INVALID_USERNAME_OR_PASSWORD_ERROR)

    def __str__(self):
        return (f"\nuser_id: {self.user_id}"
                f"\nusername: {self.username}")


if __name__ == '__main__':
    db_manager_obj = db_manager.DBManager(cursor_type='RealDictCursor')
    with db_manager_obj as cur:
        user = User("shahram", "1234")
        # user.register(cur)
        print(User.login("pedi", "1234", cur))
        print(User.login("edi", "1234", cur))
