import datetime


class BankTransaction:
    table_name = 'transactions'

    def __init__(self, transaction_type, amount, account_id, account_id_other=None, transaction_id=None,
                 date_time=None):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_id = account_id
        self.account_id_other = account_id_other
        self.date_time = datetime.datetime.now() if not date_time else date_time

    @staticmethod
    def display_transaction_list(transaction_list):
        if not transaction_list:
            raise ValueError("There is no transaction for this account ID")
        fields = '\n' + 'transaction_type'.center(20) + '|' + 'amount'.center(15) + '|' + 'date'.center(15)
        seperator = ('-' * 20) + '+' + ('-' * 15) + '+' + ('-' * 15)
        print(fields)
        for transaction in transaction_list:
            print(seperator)
            print(transaction)

    def __str__(self):
        return (f'{self.transaction_type}'.center(20) + '|' +
                f'{self.amount} $'.center(15) + '|' +
                f'{self.date_time}'.center(15))
