class Messages:
    # user
    INVALID_USERNAME_OR_PASSWORD_ERROR = "\033[91mInvalid username or password\033[0m"
    USERNAME_ALREADY_EXISTS_ERROR = "\033[91mThe username '{}' already exists.\033[0m"

    # bank_account
    NOT_ENOUGH_BALANCE_ERROR = "\033[91mNot Enough Balance.\033[0m"

    # menu
    MAIN_MENU = ("\n--------- ( main menu ) ---------- "
                 "\n0. Quit"
                 "\n1. Register "
                 "\n2. Login "
                 "\n\n Your choice: ")

    USER_MENU = ("\n--------- ( user menu ) ---------- "
                 "\n0. Logout"
                 "\n1. Create_account "
                 "\n2. Deposit "
                 "\n3. Withdraw "
                 "\n4. Transfer"
                 "\n5. Show My Accounts "
                 "\n\n Your choice: ")
