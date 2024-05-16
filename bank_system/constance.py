from collections import namedtuple

# user
MAXIMUM_USERNAME_LENGTH = 50

# other
RESPONSE = namedtuple('response', ['message', 'value', 'boolean_value'])
EMPTY_RESPONSE = RESPONSE(message='', value=None, boolean_value=False)