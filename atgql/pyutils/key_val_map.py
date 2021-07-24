__all__ = ['key_val_map']

from collections.abc import Callable, Sequence
from typing import Final, TypeVar

from atgql.pyutils.obj_map import ObjMap

T = TypeVar('T')
V = TypeVar('V')


def key_val_map(
    array: Sequence[T], key_fn: Callable[[T], str], val_fn: Callable[[T], V]
) -> ObjMap[V]:
    """
    Creates a keyed dict from an array, given a function to produce the keys
    and a function to produce the values from each item in the array.
    """

    result: Final[dict] = {}
    for item in array:
        result[key_fn(item)] = val_fn(item)
    return result
