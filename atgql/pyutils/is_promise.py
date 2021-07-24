__all__ = ['is_promise']

import inspect
from typing import TypeVar

from typing_extensions import TypeGuard

from atgql.pyutils.promise_or_value import PromiseOrValue
from atgql.shims import Promise

T = TypeVar('T')


def is_promise(value: PromiseOrValue[T]) -> TypeGuard[Promise[T]]:
    """Return True if the object can be used in await expression.

    Generator-based coroutines are awaitables,
    even though they do not have an __await__() method.
    """
    return inspect.isawaitable(value)
