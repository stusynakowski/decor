"""Apply decorators to a function at call time instead of at definition time.

    @decor
    def add(a, b):
        return a + b

    add(1, 2)                          # plain call, no decorators
    add[logged, retry(3)](1, 2)        # decorate for this call only

Decorators in the list are applied like stacked ``@`` lines, so
``add[d1, d2]`` is equivalent to ``d1(d2(add))``.
"""

import functools

__all__ = ["decor"]


class decor:
    def __init__(self, func):
        self.__wrapped__ = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __getitem__(self, decorators):
        # f[d1, d2] passes a tuple; f[d1] passes the decorator itself.
        if not isinstance(decorators, tuple):
            decorators = (decorators,)
        func = self.__wrapped__
        for decorator in reversed(decorators):
            func = decorator(func)
        return func

    def __get__(self, instance, owner=None):
        # Support use on methods: bind the instance like a normal function would.
        if instance is None:
            return self
        return decor(self.__wrapped__.__get__(instance, owner))
