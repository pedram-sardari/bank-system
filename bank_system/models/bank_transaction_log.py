from typing import Self
from .bank_transaction import BankTransaction


class BankTransactionLog(BankTransaction):
    def __init__(self, transaction_type, amount, account_id, transaction_result=None, error_message=None,
                 account_id_other=None, log_id=None):
        super().__init__(transaction_type, amount, account_id, account_id_other)
        del self.transaction_id
        self.log_id = log_id
        self.transaction_result = transaction_result
        self.error_message = error_message

    @classmethod
    def from_transaction_obj(cls, transaction: BankTransaction, transaction_result: str, error_message=None) -> Self:
        transaction_attributes = transaction.__dict__
        transaction_attributes.pop('transaction_id')
        return cls(transaction_result=transaction_result, error_message=error_message, **transaction_attributes)
