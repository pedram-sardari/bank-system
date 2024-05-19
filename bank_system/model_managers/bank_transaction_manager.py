from .model_manager import ModelManager
from ..db import db_queries as q
from ..models.bank_transaction import BankTransaction


class BankTransactionManager(ModelManager):
    def __init__(self, db_manager):
        super().__init__(db_manager, BankTransaction.table_name, BankTransaction)

    def save(self, transaction: BankTransaction):
        if not transaction.transaction_id:
            query = q.SAVE_NEW_TRANSACTION
            params = (transaction.transaction_type,
                      transaction.amount,
                      transaction.date_time,
                      transaction.account_id,
                      transaction.account_id_other)
            with self.db_manager as cursor:
                cursor.execute(query, params)
