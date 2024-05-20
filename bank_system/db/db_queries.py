TRANSACTIONS = ("deposit", "withdrawal", "transfer")

# create table queries
CREATE_TABLE_USER = """
CREATE TABLE IF NOT EXISTS users (
user_id SERIAL PRIMARY KEY,
username VARCHAR(50) NOT NULL UNIQUE, 
password VARCHAR(64) NOT NULL);"""

CREATE_TABLE_ACCOUNT = """
CREATE TABLE IF NOT EXISTS accounts ( account_id SERIAL PRIMARY KEY, 
balance DECIMAL(10, 2) NOT NULL DEFAULT 0, 
user_id INT NOT NULL, 
FOREIGN KEY (user_id) REFERENCES users(user_id));"""

CREATE_TABLE_TRANSACTION = f"""
CREATE TABLE IF NOT EXISTS transactions ( 
transaction_id SERIAL PRIMARY KEY, 
transaction_type VARCHAR(10) CHECK(transaction_type IN {TRANSACTIONS}), 
amount DECIMAL(10, 2) NOT NULL,
date_time TIMESTAMP NOT NULL,
account_id INT NOT NULL, 
account_id_other INT, 
FOREIGN KEY (account_id) REFERENCES accounts(account_id), 
FOREIGN KEY (account_id_other) REFERENCES accounts(account_id))"""

CREATE_TABLE_TRANSACTION_LOG = f"""
CREATE TABLE IF NOT EXISTS transaction_log ( 
log_id SERIAL PRIMARY KEY, 
transaction_type VARCHAR(10) CHECK(transaction_type IN {TRANSACTIONS}), 
amount DECIMAL(10, 2) NOT NULL, 
date_time TIMESTAMP NOT NULL, 
account_id INT NOT NULL, 
account_id_other INT, 
transaction_result VARCHAR(10) CHECK(transaction_status IN ('failed', 'successful')), 
error_message TEXT, 
FOREIGN KEY (account_id) REFERENCES accounts(account_id), 
FOREIGN KEY (account_id_other) REFERENCES accounts(account_id))""" 

# insert queries
SAVE_NEW_USER = "INSERT INTO users (username, password) VALUES (%s, %s)"

SAVE_NEW_ACCOUNT = "INSERT INTO accounts (balance, user_id) VALUES (%s, %s) RETURNING account_id"

SAVE_NEW_TRANSACTION = """
INSERT INTO transactions (transaction_type, amount, date_time, account_id, account_id_other)  
VALUES (%s, %s, %s, %s, %s)"""

SAVE_NEW_TRANSACTION_LOG = """
INSERT INTO transaction_log  
(transaction_type, amount, date_time, account_id, account_id_other, transaction_result, error_message) 
VALUES (%s, %s, %s, %s, %s, %s, %s)"""

# update queries
UPDATE_ACCOUNT_BALANCE = "UPDATE accounts SET balance = %s WHERE account_id = %s RETURNING account_id"
UPDATE_USER_PASSWORD = "UPDATE users SET password = %s WHERE user_id = %S"

# fetch queries
ALL = "SELECT * FROM {}"
WHERE = " WHERE "
AND = ' AND '
BY_COLUMN = '{} = %s'

