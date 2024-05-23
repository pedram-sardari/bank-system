import hashlib

from .bank_account import BankAccount


class User:
    table_name = 'users'
    manager = None

    def __init__(self, username, password=None, user_id=None):
        self.user_id = user_id
        self.username = username  # TODO: unique username
        self.password = password
        self.account_list: list[BankAccount] = []

    @staticmethod
    def hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        if len(new_password) < 64:
            self._password = User.hash_password(new_password)
        else:
            self._password = new_password

    def check_password(self, new_password):
        return self._password == self.hash_password(new_password)

    def find_my_account_by_id(self, account_id):
        if account_id.isdigit():
            for account in self.account_list:
                if account.account_id == int(account_id):
                    return account
        raise ValueError(f"You don't have andy account with id {account_id}")

    def add_new_account(self, account: BankAccount):
        self.account_list.append(account)

    def __str__(self):
        return (f"\nuser_id: {self.user_id}"
                f"\nusername: {self.username}\n")
