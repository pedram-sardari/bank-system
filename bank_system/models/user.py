import hashlib
from typing import Self
from .response import Response
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
        response = Response()
        response.bool_value = True
        if user_id:
            response.message = m.Messages.USERNAME_ALREADY_EXISTS_ERROR.format(self.username)
            response.bool_value = False
        if len(self.username) > c.MAXIMUM_USERNAME_LENGTH:
            response.message = "Username must be less than {} characters".format(50)
            response.bool_value = False
        return response

    def register(self, cursor):
        """TODO: insert query /
         TOD0: error handling -> long-string / duplicated username"""
        response = self.validate_username(cursor)
        if response.bool_value:
            cursor.execute(q.REGISTER_NEW_USER, (self.username, self.password))
            response.message = "You are successfully registered."
        return response

    @classmethod
    def login(cls, username, password, cursor):
        hashed_password = User.hash_password(password)
        cursor.execute(q.LOGIN_USER, (username, hashed_password))
        user_record = cursor.fetchone()
        response = Response()
        if user_record:
            response.bool_value = True
            response.value = cls(**user_record)
            response.message = "You are successfully logged in"
        else:
            response.message = m.Messages.INVALID_USERNAME_OR_PASSWORD_ERROR
        return response


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
