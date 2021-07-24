from typing import Any, Iterable

from typing_extensions import TypeGuard


def is_iterable_object(maybe_iterable: Any) -> TypeGuard[Iterable[Any]]:
    """
    Returns true if the provided object is an Object (i.e. not a string literal)
    and implements the Iterator protocol.
    """

    return not isinstance(maybe_iterable, str) and isinstance(maybe_iterable, Iterable)
