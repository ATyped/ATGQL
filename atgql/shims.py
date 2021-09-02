__all__ = ['Promise', 'typeof']


import types
from abc import ABC
from collections.abc import Awaitable, Callable, Iterable, MutableSequence
from inspect import getmembers, isclass, signature
from typing import Any, Generic, Literal, Optional, TypeVar, Union, cast, overload
from typing_extensions import TypeGuard

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
        # In Python3.9, mypy reports: Module has no attribute "CellType"  [attr-defined]
        # But actually it is there.
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


U = TypeVar('U')
S = TypeVar('S')


class Array(MutableSequence[T], ABC, Generic[T]):
    @staticmethod
    def is_array(value: Any) -> TypeGuard['MutableSequence[T]']:
        return isinstance(value, MutableSequence) and not isinstance(value, str)

    @overload
    @staticmethod
    def from_(
        iterable: Iterable[T], map_fn: Callable[[S, T], U], self_arg: S, /
    ) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(
        iterable: Iterable[T], map_fn: Callable[[S, T, int], U], self_arg: S, /
    ) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[T], /) -> MutableSequence[T]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[T], map_fn: Callable[[T], U], /) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[T], map_fn: Callable[[T, int], U], /) -> MutableSequence[U]:
        ...

    # mypy: Overloaded function implementation does not accept all possible arguments of signature 5
    # pyright: 0 error, 0 warnings, 0 infos
    @staticmethod  # type: ignore[misc]
    def from_(
        iterable: Iterable[T],
        map_fn: Optional[
            Union[
                Callable[[S, T], U],
                Callable[[S, T, int], U],
                Callable[[T], U],
                Callable[[T, int], U],
            ]
        ] = None,
        self_arg: Optional[S] = None,
        /,
    ) -> Any:
        if self_arg is not None:
            map_fn = cast(Optional[Union[Callable[[S, T], U], Callable[[S, T, int], U]]], map_fn)

            if map_fn is None:
                raise ValueError('`map_fn` cannot be None when `self_arg` is not None.')

            # https://docs.python.org/3/howto/descriptor.html#functions-and-methods
            bound_map_fn = cast(
                Union[Callable[[T], U], Callable[[T, int], U]],
                types.MethodType(map_fn, self_arg),
            )

            # bound method's signature will lost self argument
            param_count_without_self = len(signature(bound_map_fn).parameters)

            if param_count_without_self == 1:
                bound_map_fn = cast(Callable[[T], U], bound_map_fn)

                return [bound_map_fn(e) for e in iterable]  # pylint: disable=not-callable

            else:
                bound_map_fn = cast(Callable[[T, int], U], bound_map_fn)

                return [
                    bound_map_fn(e, i) for i, e in enumerate(iterable)  # pylint: disable=not-callable
                ]

        else:
            map_fn = cast(Optional[Union[Callable[[T], U], Callable[[T, int], U]]], map_fn)

            if map_fn is None:
                return list(iterable)

            else:
                param_count = len(signature(map_fn).parameters)

                if param_count == 1:
                    map_fn = cast(Callable[[T], U], map_fn)

                    return [map_fn(e) for e in iterable]

                else:
                    map_fn = cast(Callable[[T, int], U], map_fn)

                    return [map_fn(e, i) for i, e in enumerate(iterable)]
