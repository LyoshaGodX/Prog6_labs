import functools
import timeit
from scipy.special import factorial as f2
import json


def memoized(func):
    cache = {}

    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = args + tuple(kwargs.items())
        start_time = timeit.default_timer()

        if key not in cache:
            result = func(*args, **kwargs)
            cache[key] = result

        end_time = timeit.default_timer()
        execution_time = (end_time - start_time) * 1000
        return cache[key], execution_time

    return inner


def just_timed(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = (end_time - start_time) * 1000
        return result, execution_time

    return inner


@just_timed
def factorial_no_cashe(n):
    return f2(n)


@memoized
def factorial_cashe(n):
    return f2(n)


@memoized
def factorial_cashe_copy(n):
    return f2(n)


def save_cache(cache, filename):
    cache_str_keys = {str(key): value for key, value in cache.items()}
    with open(filename, 'w') as file:
        json.dump(cache_str_keys, file)


def load_cache(filename, func):
    with open(filename, 'r') as file:
        cache = json.load(file)
        func.__closure__[0].cell_contents = {eval(key): value for key, value in cache.items()}
        return None


def get_cache(func):
    return func.__closure__[0].cell_contents
