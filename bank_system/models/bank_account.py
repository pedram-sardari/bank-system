import datetime

from psycopg2 import extras
from ..db import db_manager
from ..db import queries as q
from .. import messages as m


class BankAccount:
    def __init__(self, balance: float, user_id: int):
        self.balance = balance  # TODO: balance should be a positive float / minimum balance
        self.user_id = user_id  # user_id or username?

    # TODO: add return result_message to functions
    def create_account(self, cursor):
        """Insert this account to accounts table in database"""
        cursor.execute(q.CREATE_NEW_ACCOUNT, (self.balance, self.user_id))

    @staticmethod
    def timestamp():
        return datetime.datetime.now()

    # TODO: amount must be positive float
    @staticmethod
    def deposit(account_id, current_balance, amount, cursor):
        new_balance = current_balance + amount
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, account_id))
        cursor.execute(q.SAVE_TRANSACTION, ('deposit', amount, BankAccount.timestamp(), account_id, None))

    @staticmethod
    def withdraw(account_id, current_balance, amount, cursor):
        # TODO: In case of minimum balance consider minimum balance instead of 0
        new_balance = current_balance - amount
        if new_balance < 0:
            raise ValueError(m.Messages.NOT_ENOUGH_BALANCE_ERROR)
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, account_id))
        cursor.execute(q.SAVE_TRANSACTION, ('withdrawal', -amount, BankAccount.timestamp(), account_id, None))

    @staticmethod
    def transfer(account_id_from, account_id_to, current_balance_from, current_balance_to, amount, cursor):
        # TODO: save the transaction
        """:raise not enough balance"""
        new_balance_from = current_balance_from - amount
        if new_balance_from < 0:
            raise ValueError(m.Messages.NOT_ENOUGH_BALANCE_ERROR)
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance_from, account_id_from))
        new_balance_to = current_balance_to + amount
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance_to, account_id_to))
        cursor.execute(q.NEXT_TRANSACTION_ID)
        transaction_id_from = cursor.fetchone()
        print(type(transaction_id_from), transaction_id_from)


if __name__ == "__main__":
    account = BankAccount(50.2, 2)
    with db_manager.DBManager() as db:
        # account.create_account(db.cursor)
        # BankAccount.deposit(1, 50.2, 100, db.cursor)
        BankAccount.withdraw(1, 52.2, 10, db.cursor)
        # BankAccount.withdraw(1, 150.2, 100, db.cursor)
        # BankAccount.transfer(
        #     account_id_from=1,
        #     account_id_to=2,
        #     current_balance_from=50.2,
        #     current_balance_to=50.2,
        #     amount=2,
        #     cursor=db.cursor
        # )
