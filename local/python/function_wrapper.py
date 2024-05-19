import functools


def function_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Begin {func.__name__} arguments - {args} keyword arguments - {kwargs}")
        result = func(*args, **kwargs)
        print(f"End   {func.__name__} returns - {result}")
        return result

    return wrapper
