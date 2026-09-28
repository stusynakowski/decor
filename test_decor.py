import functools

from decor import decor


def tag(label, calls):
    """Decorator factory that records the order decorators run in."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            calls.append(label)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def times(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) * n
        return wrapper
    return decorator


@decor
def add(a, b):
    return a + b


def test_plain_call():
    assert add(1, 2) == 3


def test_subscript_syntax():
    assert add[times(10)](1, 2) == 30


def test_order_matches_stacked_decorators():
    calls = []
    add[tag("outer", calls), tag("inner", calls)](1, 2)
    assert calls == ["outer", "inner"]


def test_decoration_does_not_persist():
    add[times(10)](1, 2)
    assert add(1, 2) == 3


def test_metadata_preserved():
    assert add.__name__ == "add"


def test_method():
    class C:
        def __init__(self, k):
            self.k = k

        @decor
        def scale(self, x):
            return self.k * x

    c = C(3)
    assert c.scale(2) == 6
    assert c.scale[times(10)](2) == 60

