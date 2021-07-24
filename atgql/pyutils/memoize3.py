__all__ = ['memoize3']

from collections.abc import Callable
from typing import TypeVar, Union
from weakref import WeakKeyDictionary

A1 = TypeVar('A1')
A2 = TypeVar('A2')
A3 = TypeVar('A3')
R = TypeVar('R')


class _UndefinedType:
    ...


_undefined = _UndefinedType()


def memoize3(fn: Callable[[A1, A2, A3], R]) -> Callable[[A1, A2, A3], R]:
    """Memoizes the provided three-argument function."""

    cache0: list[WeakKeyDictionary] = []

    def memoized(a1: A1, a2: A2, a3: A3) -> R:
        if len(cache0) == 0:
            cache0[0] = WeakKeyDictionary()

        cache1 = cache0[0].get(a1)
        if cache1 is None:
            cache1 = WeakKeyDictionary()
            cache0[0][a1] = cache1

        cache2 = cache1.get(a2)
        if cache2 is None:
            cache2 = WeakKeyDictionary()
            cache1[a2] = cache2

        fn_result: Union[_UndefinedType, R] = cache2.get(a3, _undefined)
        if isinstance(fn_result, _UndefinedType):
            fn_result = fn(a1, a2, a3)
            cache2[a3] = fn_result

        return fn_result

    return memoized
