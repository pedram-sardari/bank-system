from .model_manager import ModelManager
from .. import constance as c
from .. import messages as m
from ..db import db_queries as q
from ..models.user import User


class UserManager(ModelManager):
    def __init__(self, db_manager):
        super().__init__(db_manager, User.table_name, User)

    def save(self, user: User):
        if user.user_id:
            query = q.UPDATE_USER_PASSWORD
            params = (user.password, user.user_id)
        else:
            query = q.SAVE_NEW_USER
            params = (user.username, user.password)
        with self.db_manager as cursor:
            cursor.execute(query, params)

    def __validate_username(self, entered_username):
        user_id = self.get(username=entered_username)
        if user_id:
            raise ValueError(m.Messages.USERNAME_ALREADY_EXISTS_ERROR.format(entered_username))
        if len(entered_username) > c.MAXIMUM_USERNAME_LENGTH:
            raise ValueError("Username must be less than {} characters".format(50))  # TODO: move to message module

    def register(self, entered_username, entered_password):
        self.__validate_username(entered_username)
        user = self.model_class(entered_username, entered_password)
        self.save(user)
        return "You are successfully registered."

    def login(self, entered_username, entered_password):
        user = self.get(username=entered_username)
        if user and user.check_password(entered_password):
            return user
        raise ValueError("Username or password is incorrect.")
