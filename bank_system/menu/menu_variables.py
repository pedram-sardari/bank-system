from ..model_managers.user_manager import UserManager
from ..model_managers.bank_account_manager import BankAccountManager
from ..model_managers.bank_transaction_manager import BankTransactionManager


class MenuVariables:
    def __init__(self,
                 user_manager: UserManager,
                 bank_account_manager: BankAccountManager,
                 bank_transaction_manager: BankTransactionManager):
        self.user_manager = user_manager
        self.bank_account_manager = bank_account_manager
        self.bank_transaction_manager = bank_transaction_manager
        self.logged_in_user = None
