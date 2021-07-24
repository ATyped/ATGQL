__all__ = ['is_async_iterable']

from collections.abc import AsyncIterable
from typing import Any

from typing_extensions import TypeGuard


def is_async_iterable(maybe_async_iterable: Any) -> TypeGuard[AsyncIterable]:
    return isinstance(maybe_async_iterable, AsyncIterable)
