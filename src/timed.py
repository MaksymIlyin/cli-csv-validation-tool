import logging

from functools import wraps
from time import time


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = round(time() - start, 3)
        logging.info(f"{f.__name__} took {elapsed} seconds to finish")
        return result
    return wrapper
