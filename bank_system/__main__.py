"""
---------( main menu ) -------
1. Login
2. Register

---------( user menu ) -------
1. create_account(amount)
2. deposit(amount)
3. withdraw(amount)
4. transfer(dst_account_id, amount)
"""
def main_menu():
    while True:
        menu = ("\n0. Quit"
                "\n1. Register"
                "\n2. Login")
        print(menu)
        choice = input("Your choice: ")
        if choice == '0':
            break
        elif choice == '1':
            ...


if __name__ == "__main__":
    main_menu()
