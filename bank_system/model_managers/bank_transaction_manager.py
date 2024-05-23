from .model_manager import ModelManager
from ..db import db_queries as q
from ..models.bank_transaction import BankTransaction


class BankTransactionManager(ModelManager):
    def __init__(self, db_manager):
        super().__init__(db_manager, BankTransaction.table_name, BankTransaction)

    def filter(self, **kwargs):
        query = q.ALL.format(self.table_name)
        params = []
        filter_list = []
        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, tuple) and len(v) == 2:
                    min_amount = v[0]
                    max_amount = v[1]
                    if min_amount and max_amount:
                        filter_list.append(f"ABS({k}) BETWEEN %s AND %s OR {k} BETWEEN %s AND %s")
                        params.append(min_amount)
                        params.append(max_amount)
                    elif min_amount:
                        filter_list.append(f'ABS({k}) > %s')
                        params.append(min_amount)
                    elif max_amount:
                        filter_list.append(f'ABS({k}) < %s')
                        params.append(max_amount)
                else:
                    filter_list.append(q.BY_COLUMN.format(k))
                    params.append(v)
            query += q.WHERE + q.AND.join(filter_list) + ' ORDER BY ABS(amount)'
        with self.db_manager as cursor:
            cursor.execute(query, params)
            records = cursor.fetchall()
            if records:
                return [self.model_class(**record) for record in records]

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

if __name__ == '__main__':
    m = BankTransactionManager('ad')
