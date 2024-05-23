from .db.db_manager import DBManager
from .menu_old import Menu
from .menu.menu_manager import MenuGenerator, Menu
from .model_managers.bank_account_manager import BankAccountManager
from .model_managers.bank_transaction_manager import BankTransactionManager
from .model_managers.user_manager import UserManager
from .models.bank_account import BankAccount
from .models.bank_transaction import BankTransaction

db_manager = DBManager('RealDictCursor')
user_manager = UserManager(db_manager)
bank_account_manager = BankAccountManager(db_manager)
bank_transaction_manager = BankTransactionManager(db_manager)

# menu = Menu(user_manager, bank_account_manager, bank_transaction_manager)
menu_variable = {
    'logged_in_user': None,
    'user_manager': user_manager,
    "bank_account_manager": bank_account_manager,
    'bank_transaction_manager': bank_transaction_manager,
    'BankAccount': BankAccount,
    'BankTransaction': BankTransaction
}
Menu.set_menu_variables(menu_variable)
menu_generator = MenuGenerator(menu_directory_path='bank_system/menu/menus_list')
menu = menu_generator.create_composite_menu()

while True:
    try:
        menu()
        break
    except Exception as e:
        print(e)
        raise
