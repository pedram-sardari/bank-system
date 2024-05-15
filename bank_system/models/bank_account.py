import datetime
import prettytable
from typing import Self, List

from psycopg2 import extras
from ..db import db_manager
from ..db import queries as q
from .. import messages as m


class BankAccount:
    def __init__(self, balance: float, user_id: int, account_id=None):
        self.account_id = account_id
        self.balance = balance  # TODO: balance should be a positive float / minimum balance
        self.user_id = user_id  # user_id or username?

    # TODO: add return result_message to functions
    def create_account(self, cursor):
        """Insert this account to accounts table in database"""
        cursor.execute(q.CREATE_NEW_ACCOUNT, (self.balance, self.user_id))

    @classmethod
    def get_accounts(cls, cursor, user_id=None, account_id=None):
        # TODO: handle invalid ids
        query = q.GET_ACCOUNTS
        params = []
        if user_id or account_id:
            query += q.FILTER
            if user_id:
                query += q.BY_USER_ID
                params.append(user_id)
            elif account_id:
                query += q.BY_ACCOUNT_ID
                params.append(account_id)
        cursor.execute(query, params)
        account_records = cursor.fetchall()
        return [cls(**record) for record in account_records]

    @staticmethod
    def display_accounts(accounts_list):
        table = prettytable.PrettyTable()
        if accounts_list:
            table.field_names = accounts_list[0].__dict__.keys()
            rows = [account.__dict__.values() for account in accounts_list]
            table.add_rows(rows)
            print(table)

    @staticmethod
    def timestamp():
        return datetime.datetime.now()

    def transaction(self, cursor, transaction_type, amount, transaction_id_from=None):
        new_balance = self.balance + amount
        if new_balance < 0:
            raise ValueError(m.Messages.NOT_ENOUGH_BALANCE_ERROR)
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, self.account_id))
        params = (transaction_type, amount, BankAccount.timestamp(), self.account_id, transaction_id_from)
        cursor.execute(q.SAVE_TRANSACTION, params)

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
    db_manager_obj = db_manager.DBManager(cursor_type='RealDictCursor')
    with db_manager_obj as cur:
        account_obj = BankAccount(50.2, 2)
        BankAccount.display_accounts(BankAccount.get_accounts(cur, account_id=1))
        # account_obj.create_account(cur)
        # BankAccount.deposit(1, 50.2, 100, cur)
        # BankAccount.withdraw(1, 52.2, 10, cur)
        # BankAccount.withdraw(1, 150.2, 100, cur)
        # BankAccount.transfer(
        #     account_obj_id_from=1,
        #     account_obj_id_to=2,
        #     current_balance_from=50.2,
        #     current_balance_to=50.2,
        #     amount=2,
        #     cursor=cur
        # )
