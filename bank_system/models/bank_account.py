import datetime
import tabulate
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
        self.user_id = user_id

    # TODO: add return result_message to functions
    def create_account(self, cursor):
        """Insert this account to accounts table in database"""
        cursor.execute(q.CREATE_NEW_ACCOUNT, (self.balance, self.user_id))

    @staticmethod
    def __execute_query__fetch_accounts(cursor, user_id=None, account_id=None):
        # TODO: handle invalid ids
        query = q.FETCH_ACCOUNTS
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
        return cursor.fetchall()

    @classmethod
    def get_accounts(cls, cursor, user_id=None, account_id=None):
        account_records = cls.__execute_query__fetch_accounts(cursor, user_id, account_id)
        return [cls(**record) for record in account_records]

    @staticmethod
    def display_accounts(cursor, user_id=None, account_id=None):
        account_records = BankAccount.__execute_query__fetch_accounts(cursor, user_id, account_id)
        table = tabulate.tabulate(account_records, headers='keys', tablefmt='grid')
        print(table)

    @staticmethod
    def timestamp():
        return datetime.datetime.now()

    def __update_balance(self, cursor, amount):
        new_balance = self.balance + amount
        if new_balance < 0:  # TODO: In case of minimum balance consider minimum balance instead of 0
            raise ValueError(m.Messages.NOT_ENOUGH_BALANCE_ERROR)
        cursor.execute(q.UPDATE_ACCOUNT_BALANCE, (new_balance, self.account_id))

    def __execute_transaction(self, cursor, transaction_type, amount, transaction_id_from=None):
        self.__update_balance(cursor, amount)

        cursor.execute(q.NEXT_TRANSACTION_ID)
        transaction_id = cursor.fetchone()['nextval']

        params = (transaction_id, transaction_type, amount, BankAccount.timestamp(),
                  self.account_id, transaction_id_from)
        print(params)
        cursor.execute(q.SAVE_TRANSACTION, params)
        return transaction_id

    # TODO: amount must be positive float
    def deposit(self, cursor, amount):
        self.__execute_transaction(cursor, 'deposit', amount)

    def withdraw(self, cursor, amount):
        """:raise not enough balance"""
        self.__execute_transaction(cursor, 'withdrawal', -amount)

    def transfer(self, cursor, amount, another_account: Self):
        # TODO: save the transaction
        """:raise not enough balance"""
        transaction_id_from = self.__execute_transaction(cursor, 'transfer', -amount)
        another_account.__execute_transaction(cursor, 'transfer', amount, transaction_id_from)

    def __str__(self):
        attr_dict = [self.__dict__]
        table = tabulate.tabulate(attr_dict, headers='keys', tablefmt='grid')
        return '\n' + str(table) + '\n'

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    db_manager_obj = db_manager.DBManager(cursor_type='RealDictCursor')
    with db_manager_obj as cur:
        account_obj = BankAccount(50.2, 2)
        BankAccount.display_accounts(cur,user_id=2)
        print(BankAccount.get_accounts(cur, user_id=2))
        account_obj_1 = BankAccount.get_accounts(cur, account_id=1)[0]
        account_obj_2 = BankAccount.get_accounts(cur, account_id=2)[0]
        # account_obj.create_account(cur)
        # account_obj_1.deposit(cur, amount=50)
        # account_obj_1.withdraw(cur, amount=10)
        # account_obj_1.withdraw(cur, amount=130)
        # account_obj_1.transfer(cur, 60, account_obj_2)
