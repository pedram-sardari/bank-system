from ..db import db_manager
from ..db import queries as q


class BankAccount:
    def __init__(self, balance: float, user_id: int):
        self.balance = balance  # TODO: balance should be a positive float / minimum balance
        self.user_id = user_id  # user_id or username?

    def create_account(self, cursor):
        """Insert this account to accounts table in database"""
        cursor.execute(q.CREATE_NEW_ACCOUNT, (self.balance, self.user_id))

    # TODO: amount must be positive float
    @staticmethod
    def deposit(account_id, current_balance, amount, cursor):
        new_balance = current_balance + amount
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, account_id))

    @staticmethod
    def withdraw(account_id, current_balance, amount, cursor):
        # TODO: In case of minimum balance consider minimum balance instead of 0
        new_balance = current_balance - amount
        if new_balance < 0:
            raise ValueError()  # TODO: proper error message
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, account_id))

    @staticmethod
    def transfer():
        ...


if __name__ == "__main__":
    account = BankAccount(50.2, 1)
    with db_manager.DBManager() as db:
        # account.create_account(db.cursor)
        # BankAccount.deposit(1, 50.2, 100, db.cursor)
        BankAccount.withdraw(1, 150.2, 100, db.cursor)
    # TODO: test all account class methods.





