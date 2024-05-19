import datetime


class BankTransaction:
    table_name = 'transactions'

    def __init__(self, transaction_type, amount, account_id, account_id_other=None, transaction_id=None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_id = account_id
        self.account_id_other = account_id_other
        self.date_time = datetime.datetime.now()
