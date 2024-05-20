import logging
from functools import wraps
from .models.bank_transaction_log import BankTransactionLog
from .db import db_queries as q
from .db.db_manager import DBManager


class Logger:
    def __init__(self, log_file, log_level=logging.DEBUG):
        self.logger = self._setup_logger(log_file, log_level)

    def _setup_logger(self, log_file, log_level):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(log_level)

        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self._call_func(func, *args, **kwargs)

        return wrapper

    def _call_func(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            log_message = self._generate_log_message(func, args, kwargs, return_value=result)
            self.logger.info(log_message)
            return result
        except Exception as e:
            log_message = self._generate_log_message(func, args, kwargs, error=e)
            self.logger.warning(log_message)
            raise

    def _generate_log_message(self, func, args, kwargs, return_value=None, error: Exception = None):
        args_str = ', '.join([repr(arg) for arg in args])
        kwargs_str = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])
        all_args_str = ', '.join([args_str, kwargs_str])
        error_str = f':{error.__class__.__name__}({error})' if error else ""
        return f"{func.__name__}({all_args_str}) -> {str(return_value)} {error_str}"


class BankLogger(Logger):
    def __init__(self, log_file='bank.log', log_level=logging.DEBUG):
        super().__init__(log_file, log_level)


class TransactionLogger(BankLogger):

    def _call_func(self, func, *args, **kwargs):
        transaction_log = self._generate_log_object(func, *args, **kwargs)
        try:
            # log to bank.log
            transaction = super()._call_func(func, *args, **kwargs)

            transaction_log.transaction_result = 'successful'
            return transaction
        except Exception as e:
            transaction_log.transaction_result = 'failed'
            transaction_log.error_message = str(e)
            raise
        finally:
            self._save_log_obj(transaction_log)

    def _generate_log_object(self, func, *args, **kwargs) -> BankTransactionLog:
        account = args[0]
        return BankTransactionLog(
            transaction_type='withdrawal' if func.__name__ == 'withdraw' else func.__name__,
            amount=kwargs['amount'],
            account_id=account.account_id,
            account_id_other=kwargs['another_account'].account_id if func.__name__ == 'transfer' else None
        )

    def _save_log_obj(self, transaction_log):
        with DBManager() as cursor:
            params = (
                transaction_log.transaction_type,
                transaction_log.amount,
                transaction_log.date_time,
                transaction_log.account_id,
                transaction_log.account_id_other,
                transaction_log.transaction_result,
                transaction_log.error_message
            )
            cursor.execute(q.SAVE_NEW_TRANSACTION_LOG, params)
