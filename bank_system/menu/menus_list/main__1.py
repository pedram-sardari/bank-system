"""You can log in or register in this menu"""
go_back_keyword = 'Exit'


def register__1_1(menu_variables: dict) -> str:
    """Register a new account"""
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    return menu_variables['user_manager'].register(username, password)


def log_in__1_2(menu_variables):
    """Log in with your account"""
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = menu_variables['user_manager'].login(username, password)
    menu_variables['logged_in_user'] = user
    account_list = menu_variables['bank_account_manager'].filter(user_id=user.user_id)
    if account_list:
        user.account_list = account_list
    return "You have successfully logged in."
