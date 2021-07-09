from typing import TypeVar

T = TypeVar('T')


def identity_func(x: T) -> T:
    """Returns the first argument it receives."""
    return x
