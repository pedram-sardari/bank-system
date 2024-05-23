import os
import time

from . import messages as m
from .db.db_manager import DBManager
from .model_managers.bank_account_manager import BankAccountManager
from .model_managers.bank_transaction_manager import BankTransactionManager
from .model_managers.user_manager import UserManager
from .models.bank_account import BankAccount
from .models.bank_transaction import BankTransaction
from .models.user import User


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Menu:
    def __init__(self, user_manager: UserManager, bank_account_manager: BankAccountManager,
                 bank_transaction_manager: BankTransactionManager):
        self.user_manager = user_manager
        self.bank_account_manager = bank_account_manager
        self.bank_transaction_manager = bank_transaction_manager

    def __call__(self, *args, **kwargs):
        self.main_menu()

    def main_menu(self):
        msg = "Welcome to bank"
        while True:
            clear_screen()
            print(f"{'\n' * 3}{msg}{'\n' * 3}")
            input("enter...")
            clear_screen()

            choice = input(m.Messages.MAIN_MENU)
            if choice == '0':
                break
            elif choice == '1':
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                msg = self.user_manager.register(username, password)
            elif choice == '2':
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                user = self.user_manager.login(username, password)
                account_list = self.bank_account_manager.filter(user_id=user.user_id)
                if account_list:
                    user.account_list = account_list
                print("You have successfully logged in.")
                while True:
                    try:
                        msg = self.user_menu(user)
                        break
                    except Exception as e:
                        print(e)
                        raise
            else:
                msg = "Invalid choice"

    def user_menu(self, logged_in_user: User):
        msg = f'welcome {logged_in_user.username}'
        while True:
            clear_screen()
            print(f"{'\n' * 3}{msg}{'\n' * 3}")
            input("enter...")
            clear_screen()
            choice = input(m.Messages.USER_MENU)
            if choice == '0':
                return 'See you later'
            elif choice == '1':
                initial_balance = input("Initial Balance: ")
                initial_balance = BankAccount.is_positive_number(initial_balance)
                new_account = BankAccount(balance=initial_balance, user_id=logged_in_user.user_id)
                new_account.account_id = self.bank_account_manager.save(new_account)
                logged_in_user.add_new_account(new_account)
                msg = 'successful account creation'
            elif choice == '2':
                account_id = input("Account ID: ")
                amount = input("Amount: ")
                amount = BankAccount.is_positive_number(amount)
                account = logged_in_user.find_my_account_by_id(account_id)
                transaction = account.deposit(amount=amount)
                self.bank_transaction_manager.save(transaction)
                self.bank_account_manager.save(account)
                msg = 'successful deposit'
            elif choice == '3':
                account_id = input("Account ID: ")
                amount = input("Amount: ")
                amount = BankAccount.is_positive_number(amount)
                account = logged_in_user.find_my_account_by_id(account_id)
                transaction = account.withdraw(amount=amount)
                self.bank_account_manager.save(account)
                self.bank_transaction_manager.save(transaction)
                msg = 'successful withdraw'
            elif choice == '4':
                account_id_self = input("Your Account ID: ")
                account_id_other = input("Target Account ID: ")
                amount = input("Amount: ")
                amount = BankAccount.is_positive_number(amount=amount)
                account_self = logged_in_user.find_my_account_by_id(account_id_self)
                try:
                    account_other = logged_in_user.find_my_account_by_id(account_id_other)
                except ValueError:
                    account_other = self.bank_account_manager.get(account_id=account_id_other)

                if account_self and account_other:
                    transaction_self, transaction_other = account_self.transfer(another_account=account_other,
                                                                                amount=amount)
                    # save accounts
                    self.bank_account_manager.save(account_self)
                    self.bank_account_manager.save(account_other)
                    # save transactions
                    self.bank_transaction_manager.save(transaction_self)
                    self.bank_transaction_manager.save(transaction_other)
            elif choice == '5':
                BankAccount.display_account_list(logged_in_user.account_list)
                input("\nPress any key to continue... ")
            elif choice == '6':
                account_id = input("Your Account ID: ")
                transaction_type = input("Transaction type: ")
                min_amount = input("Min amount: ").strip()
                if min_amount:
                    min_amount = BankAccount.is_positive_number(min_amount)
                max_amount = input("Max amount: ")
                if max_amount:
                    max_amount = BankAccount.is_positive_number(max_amount)
                transaction_list = self.bank_transaction_manager.filter(
                    account_id=account_id,
                    transaction_type=transaction_type,
                    amount=(min_amount, max_amount)
                )
                BankTransaction.display_transaction_list(transaction_list)



            else:
                msg = "Invalid choice"


if __name__ == "__main__":
    db_manager_obj = DBManager('RealDictCursor')
    menu = Menu(db_manager_obj)
    menu.main_menu()
