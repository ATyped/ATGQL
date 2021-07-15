from collections.abc import Callable, Sequence
from typing import Final, TypeVar

from atgql.pyutils.obj_map import ObjMap

T = TypeVar('T')


def key_map(array: Sequence[T], key_fn: Callable[[T], str]) -> ObjMap[T]:
    result: Final[dict] = {}
    for item in array:
        result[key_fn(item)] = item
    return result
