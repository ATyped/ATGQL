__all__ = ['Path', 'add_path', 'path_to_array']

from dataclasses import dataclass
from typing import Optional, Union

from atgql.pyutils.maybe import Maybe


@dataclass
class Path:
    prev: Optional['Path']
    key: Union[str, int]
    typename: Optional[str]


def add_path(prev: Optional[Path], key: Union[str, int], typename: Optional[str]) -> Path:
    """Given a Path and a key, return a new Path containing the new key."""

    return Path(prev, key, typename)


def path_to_array(path: Maybe[Path]) -> list[Union[str, int]]:
    """Given a Path, return an Array of the path keys."""

    flattened = []
    curr = path
    while curr:
        flattened.append(curr.key)
        curr = curr.prev
    flattened.reverse()
    return flattened
