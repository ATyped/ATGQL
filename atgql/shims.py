__all__ = ['Promise', 'typeof']

import types
from collections.abc import Awaitable, Callable
from inspect import getmembers, isclass
from typing import Any, Literal, TypeVar

T = TypeVar('T')

Promise = Awaitable[T]


boolean_types = {bool}
number_types = {int, float, complex}
string_types = {str}
callable_types = set()
known_object_types = set([type(None)])
symbol_types = set()


for _name, _attr in getmembers(types, isclass):
    if _name.startswith('_'):
        continue

    if issubclass(_attr, Callable):  # type: ignore[arg-type]
        callable_types.add(_attr)
    elif _attr in (
        types.CellType,  # type: ignore[attr-defined]
        types.ModuleType,
        types.MappingProxyType,
        types.SimpleNamespace,
    ):
        known_object_types.add(_attr)
    else:
        symbol_types.add(_attr)


def typeof(value: Any) -> Literal['object', 'boolean', 'number', 'string', 'function', 'symbol']:
    """The simulator of `typeof` in JavaScript.

    JavaScript-side:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof#description

    Python-side:
    https://docs.python.org/3/library/types.html#standard-interpreter-types

    Precondition:

    | Types / Values                                                    | Result     |
    |-------------------------------------------------------------------|------------|
    | None                                                              | 'object'   |
    | only `bool`, no subclasses                                        | 'boolean'  |
    | only `int` / `float` / `complex`, no subclasses                   | 'number'   |
    | only `str`, no subclasses                                         | 'string'   |
    | the types which is subclass of `Callable` in module `types`       | 'function' |
    | `CellType` / `ModuleType` / `MappingProxyType`/ `SimpleNamespace` | 'object'   |
    | the other types in module `types`                                 | 'symbol'   |
    | any others                                                        | 'object'   |

    Notes:

    The reason why `CellType`, `ModuleType`, `MappingProxyType` and `SimpleNamespace`
    are considered to be 'object', is that users can manually control its properties,
    and `MappingProxyType`, which is seen as `dict`, is like the literal style in
    JavaScript that defines object.
    """

    t = type(value)

    if t in boolean_types:
        return 'boolean'
    elif t in number_types:
        return 'number'
    elif t in string_types:
        return 'string'
    elif t in callable_types:
        return 'function'
    elif t in symbol_types:
        return 'symbol'
    elif t in known_object_types:
        return 'object'
    else:
        return 'object'
