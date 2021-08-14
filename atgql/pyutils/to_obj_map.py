__all__ = ['to_obj_map']

from collections.abc import Mapping
from typing import TypeVar, overload

from atgql.pyutils.obj_map import ObjMap, ObjMapLike, ReadOnlyObjMap, ReadOnlyObjMapLike

T = TypeVar('T')


@overload
def to_obj_map(obj: ObjMapLike[T]) -> ObjMap[T]:  # type: ignore[misc]
    # Here mypy complains `for:
    # "Overloaded function signatures 1 and 2 overlap with incompatible return types".
    # That's wrong, because:
    # ObjMapLike is a subclass of ReadOnlyObjMapLike, and
    # ObjMap is a subclass of ReadOnlyObjMap
    ...


@overload
def to_obj_map(obj: ReadOnlyObjMapLike[T]) -> ReadOnlyObjMap[T]:
    ...


def to_obj_map(obj):
    """Convert an object to dict by iterating its attributes.

    Internally it will call vars() if the argument is not a dict,
    vars() will return the object's __dict__.

    In the implementation of graphql-js, toObjMap() uses Object.entries(),
    which returns an array of a given object's own enumerable string-keyed property.

    Enumerable properties are usually created via simple assignment or via a property initializer,
    as for Python, these operations are reflected by __dict__.

    References:

    https://docs.python.org/3/library/functions.html?#vars

    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries

    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Enumerability_and_ownership_of_properties
    """

    if isinstance(obj, Mapping):
        return obj
    else:
        return dict(vars(obj).items())  # shallow copy, also typecast
