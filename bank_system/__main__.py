from .db.db_manager import DBManager
from .menu import Menu
from .model_managers.bank_account_manager import BankAccountManager
from .model_managers.bank_transaction_manager import BankTransactionManager
from .model_managers.user_manager import UserManager

db_manager = DBManager('RealDictCursor')
user_manager = UserManager(db_manager)
bank_account_manager = BankAccountManager(db_manager)
bank_transaction_manager = BankTransactionManager(db_manager)

menu = Menu(user_manager, bank_account_manager, bank_transaction_manager)

while True:
    try:
        menu()
        break
    except Exception as e:
        print(e)
        # raise

