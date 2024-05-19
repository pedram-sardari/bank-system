from .model_manager import ModelManager
from ..db import db_queries as q
from ..models.bank_account import BankAccount


class BankAccountManager(ModelManager):
    def __init__(self, db_manager):
        super().__init__(db_manager, BankAccount.table_name, BankAccount)

    def save(self, account: BankAccount):
        if account.account_id:
            query = q.UPDATE_ACCOUNT_BALANCE
            params = (account.balance, account.account_id)
        else:
            query = q.SAVE_NEW_ACCOUNT
            params = (account.balance, account.user_id)
        with self.db_manager as cursor:
            cursor.execute(query, params)  # TODO: handle failed creation
            account_id_dict = cursor.fetchone()
            return account_id_dict['account_id']
