# import logging
#
# # class Logger:
# #     def __init__(self)
#
# i = 2
# formatter = logging.Formatter(f'{i}%(asctime)s:%(name)s:%(filename)s:%(module)s:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler('bank.log')
# file_handler.setLevel(logging.WARNING)
# file_handler.setFormatter(formatter)
#
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.ERROR)
# stream_handler.setFormatter(formatter)
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)
#
# logger.info('info')
# logger.debug('debug')
# logger.warning('warning')
# logger.error('error')
#
# logger2 = logging.getLogger('__pedi__')
# logger2.addHandler(file_handler)
#
# logger2.error('error.__pedi__')
#


class A:
    def __init__(self):
        self.b = 2

    @property
    def b(self):
        return self.b + 1


print(A().b())
