import decimal
from typing import Self

from .bank_transaction import BankTransaction
from .. import messages as m
from ..db import db_manager


class BankAccount:
    table_name = 'accounts'

    def __init__(self, balance: decimal.Decimal, user_id: int, account_id=None):
        self.account_id = account_id
        self.balance = balance  # TODO: balance should be a positive float / minimum balance
        self.user_id = user_id

    @staticmethod
    def is_positive_number(amount: str) -> decimal.Decimal:
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Invalid input (Must be a positive number)")
        else:
            return decimal.Decimal(amount)

    @staticmethod
    def display_account_list(account_list):
        fields = '\n' + 'account_id'.center(15) + '|' + 'balance'.center(15)
        seperator = ('-' * 15) + '+' + ('-' * 15)
        print(fields)
        if not account_list:
            raise ValueError("You don't have any account in the bank!")
        for account in account_list:
            print(seperator)
            print(account)

    def __update_balance(self, amount: decimal.Decimal):
        new_balance = self.balance + amount
        if new_balance < 0:  # TODO: In case of minimum balance consider minimum balance instead of 0
            raise ValueError(m.Messages.NOT_ENOUGH_BALANCE_ERROR)
        self.balance = new_balance

    def deposit(self, amount: decimal.Decimal):
        self.__update_balance(amount)
        return BankTransaction(transaction_type='deposit', amount=amount, account_id=self.account_id)

    def withdraw(self, amount: decimal.Decimal):
        self.__update_balance(-amount)
        return BankTransaction(transaction_type='withdrawal', amount=-amount, account_id=self.account_id)

    def transfer(self, another_account: Self, amount: decimal.Decimal):
        self.__update_balance(-amount)
        another_account.__update_balance(amount)
        transaction_self = BankTransaction(transaction_type='transfer', amount=-amount, account_id=self.account_id,
                                           account_id_other=another_account.account_id)
        transaction_another = BankTransaction(transaction_type='transfer', amount=amount,
                                              account_id=another_account.account_id, account_id_other=self.account_id)
        return transaction_self, transaction_another

    def __str__(self):
        return f'{self.account_id}'.center(15) + '|' + f'{self.balance} $'.center(15)

    def __repr__(self):
        return str(self)


