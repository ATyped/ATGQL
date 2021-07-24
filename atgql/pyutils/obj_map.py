__all__ = ['ObjMap', 'ObjMapLike', 'ReadOnlyObjMap', 'ReadOnlyObjMapLike']

from collections.abc import Mapping, MutableMapping
from typing import TypeVar

T = TypeVar('T')

ObjMap = MutableMapping[str, T]
ObjMapLike = ObjMap[T]

ReadOnlyObjMap = Mapping[str, T]
ReadOnlyObjMapLike = ReadOnlyObjMap[T]
