import time
from functools import wraps
import cProfile
import numpy as np

def handicraft_timer(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("time elapsed for", func.__name__,":", end-start)
        return result
    return wrapper

def handicraft_profiler(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("the profile for", func.__name__,":")
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.print_stats(sort="calls")
        pr.disable()
        return result
    return wrapper


def handicraft_exception_handler(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        with np.errstate(all='ignore'):
            result = func(*args, **kwargs)
        return result
    return wrapper