"""You can manage your account in this menu"""
go_back_keyword = 'Log Out'


def display_my_accounts__1_2_1(menu_variables):
    """View all your accounts in our bank"""
    menu_variables['BankAccount'].display_account_list(menu_variables['logged_in_user'].account_list)
    return ''


def create_new_account__1_2_2(menu_variables):
    """create a new account by choosing a username and password."""
    initial_balance = input("Initial Balance: ")
    initial_balance = menu_variables['BankAccount'].is_positive_number(initial_balance)
    new_account = menu_variables['BankAccount'](balance=initial_balance,
                                                user_id=menu_variables['logged_in_user'].user_id)
    new_account.account_id = menu_variables['bank_account_manager'].save(new_account)
    menu_variables['logged_in_user'].add_new_account(new_account)
    return 'successful account creation'


def deposit__1_2_3(menu_variables):
    """Deposit an amount of money into your account."""
    account_id = input("Account ID: ")
    amount = input("Amount: ")
    amount = menu_variables['BankAccount'].is_positive_number(amount)
    account = menu_variables['logged_in_user'].find_my_account_by_id(account_id)
    transaction = account.deposit(amount=amount)
    menu_variables['bank_account_manager'].save(account)
    menu_variables['bank_transaction_manager'].save(transaction)
    return 'successful deposit'


def withdraw__1_2_4(menu_variables):
    """withdraw an amount of money from your account."""
    account_id = input("Account ID: ")
    amount = input("Amount: ")
    amount = menu_variables['BankAccount'].is_positive_number(amount)
    account = menu_variables['logged_in_user'].find_my_account_by_id(account_id)
    transaction = account.withdraw(amount=amount)
    menu_variables['bank_account_manager'].save(account)
    menu_variables['bank_transaction_manager'].save(transaction)
    return 'successful withdrawal'


def transfer__1_2_5(menu_variables):
    """Transfer an amount of money from your account to another account"""
    account_id_self = input("Your Account ID: ")
    account_id_other = input("Target Account ID: ")
    amount = input("Amount: ")
    amount = menu_variables['BankAccount'].is_positive_number(amount=amount)
    account_self = menu_variables['logged_in_user'].find_my_account_by_id(account_id_self)
    try:
        account_other = menu_variables['logged_in_user'].find_my_account_by_id(account_id_other)
    except ValueError:
        account_other = menu_variables['bank_account_manager'].get(account_id=account_id_other)

    if account_self and account_other:
        transaction_self, transaction_other = account_self.transfer(another_account=account_other, amount=amount)
        # save accounts
        menu_variables['bank_account_manager'].save(account_self)
        menu_variables['bank_account_manager'].save(account_other)
        # save transactions
        menu_variables['bank_transaction_manager'].save(transaction_self)
        menu_variables['bank_transaction_manager'].save(transaction_other)
        return 'Successful transfer'
    raise ValueError('Invalid target account ID')


def display_transactions__1_2_6(menu_variables):
    """See one of your accounts transactions based on a specific filter"""
    account_id = input("Your Account ID: ")
    transaction_type = input("Transaction type: ")
    min_amount = input("Min amount: ").strip()
    if min_amount:
        min_amount = menu_variables['BankAccount'].is_positive_number(min_amount)
    max_amount = input("Max amount: ")
    if max_amount:
        max_amount = menu_variables['BankAccount'].is_positive_number(max_amount)
    transaction_list = menu_variables['bank_transaction_manager'].filter(
        account_id=account_id,
        transaction_type=transaction_type,
        amount=(min_amount, max_amount)
    )
    menu_variables['BankTransaction'].display_transaction_list(transaction_list)
    return ''
