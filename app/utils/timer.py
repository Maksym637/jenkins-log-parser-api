import time


def timeit(func: "function") -> "function":
    def wrapper(*args: object, **kwargs: object) -> "function":
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return result, elapsed_time

    return wrapper
