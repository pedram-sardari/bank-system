import os
import time

from .models.response import Response
from .db.db_manager import DBManager
from . import messages as m
from .models.user import User
from .models.bank_account import BankAccount

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu(db_manager):
    while True:
        # clear_screen()
        choice = input(m.Messages.MAIN_MENU)
        if choice == '0':
            break
        elif choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            with db_manager as cursor:
                user = User(username, password)
                response = user.register(cursor)
        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            with db_manager as cursor:
                response = User.login(username, password, cursor)
                if response.bool_value:
                    logged_in_user = response.value
                    response = user_menu(db_manager, logged_in_user, response)
        else:
            response = Response(message="Invalid choice")

        # clear_screen()
        print(f"{'\n'*3}{response.message}{'\n'*3}")
        time.sleep(4)


def user_menu(db_manager, logged_in_user, response):
    while True:
        clear_screen()
        print(f"{'\n'*3}{response.message}{'\n'*3}")
        time.sleep(4)
        clear_screen()
        choice = input(m.Messages.USER_MENU)
        if choice == '0':
            return Response(message='See you later')
        elif choice == '1':
            initial_balance = input("Initial Balance: ")
            response = BankAccount.validate_amount(initial_balance)
            if response.bool_value:
                initial_balance = response.value
                new_account = BankAccount(initial_balance, logged_in_user.user_id)
                with db_manager as cursor:
                    response = new_account.create_account(cursor)
        elif choice == '2':
            amount = input("Amount: ")
        else:
            response = Response(message="Invalid choice")



if __name__ == "__main__":
    db_manager_obj = DBManager('RealDictCursor')
    main_menu(db_manager_obj)
