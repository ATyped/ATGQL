__all__ = ['ObjMap', 'ObjMapLike', 'ReadOnlyObjMap', 'ReadOnlyObjMapLike']

from collections.abc import Mapping, MutableMapping
from typing import TypeVar, Union

T = TypeVar('T')


ObjMap = MutableMapping[str, T]
# We cannot assume an object is writable, ...
ObjMapLike = ObjMap[T]

ReadOnlyObjMap = Mapping[str, T]
# ..., but we can assume an object is readable,
# otherwise using this library will be nonsense.
ReadOnlyObjMapLike = Union[ReadOnlyObjMap[T], object]


# Although issubclass cannot be used on parameterized generic,
# ObjMap is a subclass of ReadOnlyObjMap, and ObjMapLike is a subclass of ReadOnlyObjMapLike
