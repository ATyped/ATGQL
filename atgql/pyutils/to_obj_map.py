__all__ = ['to_obj_map']

from typing import TypeVar, Union, overload

from atgql.pyutils.obj_map import ObjMap, ObjMapLike, ReadOnlyObjMap, ReadOnlyObjMapLike

T = TypeVar('T')


@overload
def to_obj_map(obj: ObjMapLike[T]) -> ObjMap[T]:
    ...


@overload
def to_obj_map(obj: ReadOnlyObjMapLike[T]) -> ReadOnlyObjMap[T]:
    ...


def to_obj_map(obj: Union[ObjMapLike[T], ReadOnlyObjMapLike[T]]):
    return obj
