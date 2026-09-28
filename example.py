"""Run with: python3 example.py"""

import functools
import time

from decor import decor


# --- Some ordinary decorators ------------------------------------------------

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [log] calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"  [log] {func.__name__} returned {result}")
        return result
    return wrapper


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  [time] {func.__name__} took {time.perf_counter() - start:.6f}s")
        return result
    return wrapper


def times(n):
    """Decorator factory: multiply the result by n."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) * n
        return wrapper
    return decorator


# --- A function opted in with @decor -----------------------------------------

@decor
def add(a, b):
    return a + b


if __name__ == "__main__":
    print("1. Plain call:")
    print("  result:", add(1, 2))

    print("\n2. Bracket form  add[logged](1, 2):")
    print("  result:", add[logged](1, 2))

    print("\n3. Several decorators, one with args  add[timed, logged, times(10)](1, 2):")
    print("  result:", add[timed, logged, times(10)](1, 2))

    print("\n4. Plain call again (nothing persisted):")
    print("  result:", add(1, 2))

