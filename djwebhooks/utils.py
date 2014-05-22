import sys


def always_string(value):
    """Regardless of the Python version, this always returns a string """
    if sys.version > '3':
        return value.decode('utf-8')
    return value