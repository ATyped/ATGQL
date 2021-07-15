import inspect
from collections.abc import Awaitable
from typing import Any

from typing_extensions import TypeGuard


def is_promise(value: Any) -> TypeGuard[Awaitable]:
    """Return True if the object can be used in await expression.

    Generator-based coroutines are awaitables,
    even though they do not have an __await__() method.
    """
    return inspect.isawaitable(value)
