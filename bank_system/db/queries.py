TRANSACTIONS = ("deposit", "withdrawal", "transfer")

CREATE_TABLE_USER = ("CREATE TABLE IF NOT EXISTS users ("
                     "user_id SERIAL PRIMARY KEY,"
                     "username VARCHAR(50) NOT NULL UNIQUE,"
                     "password VARCHAR(64) NOT NULL);")

CREATE_TABLE_ACCOUNT = ("CREATE TABLE IF NOT EXISTS accounts ("
                        "account_id SERIAL PRIMARY KEY,"
                        "balance DECIMAL(10, 2) NOT NULL DEFAULT 0,"
                        "user_id INT NOT NULL,"
                        "FOREIGN KEY (user_id) REFERENCES users(user_id));")

CREATE_TABLE_TRANSACTION = (f"CREATE TABLE IF NOT EXISTS transactions ("
                            f"transaction_id SERIAL PRIMARY KEY,"
                            f"transaction_type VARCHAR(10) CHECK(transaction_type IN {TRANSACTIONS}),"
                            f"amount DECIMAL(10, 2) NOT NULL,"
                            f"date_time TIMESTAMP NOT NULL,"
                            f"account_id INT NOT NULL,"
                            f"transaction_id_from INT,"
                            f"FOREIGN KEY (transaction_id_from) REFERENCES transactions(transaction_id))")

# insert queries
REGISTER_NEW_USER = "INSERT INTO users (username, password) VALUES (%s, %s)"
CREATE_NEW_ACCOUNT = "INSERT INTO accounts (balance, user_id) VALUES (%s, %s)"
SAVE_TRANSACTION = ("INSERT INTO transactions "
                    "(transaction_id, transaction_type, amount, date_time, account_id, transaction_id_from) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")

# update queries
UPDATE_ACCOUNT_BALANCE = "UPDATE accounts SET balance = %s WHERE account_id = %s"

# fetch queries
USERNAME_EXISTENCE = "SELECT user_id FROM users WHERE username = %s"
LOGIN_USER = "SELECT * FROM users WHERE username = %s AND password = %s"
NEXT_TRANSACTION_ID = "SELECT NEXTVAL('transactions_transaction_id_seq')"
FETCH_ACCOUNTS = "SELECT * FROM accounts"
FILTER = " WHERE "
BY_USER_ID = "user_id = %s"
BY_ACCOUNT_ID = "account_id = %s"
