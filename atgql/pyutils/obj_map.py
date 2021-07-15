from collections.abc import Mapping, MutableMapping
from typing import TypeVar

T = TypeVar('T')

ObjMap = MutableMapping[str, T]
ObjMapLike = ObjMap

ReadOnlyObjMap = Mapping[str, T]
ReadOnlyObjMapLike = ReadOnlyObjMap
