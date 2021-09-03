__all__ = ['Promise', 'typeof', 'Array']


import types
from abc import ABC
from collections.abc import Awaitable, Callable, Iterable, MutableSequence
from inspect import getmembers, isclass, signature
from typing import Any, Generic, Literal, Optional, TypeVar, Union, cast, overload
from typing_extensions import TypeGuard
from numbers import Number


_T = TypeVar('_T')

Promise = Awaitable[_T]


_boolean_types = (bool,)
_number_types = (Number,)
_string_types = (str,)
_known_object_types = (
    type(None),
    # In Python3.9, mypy reports: Module has no attribute "CellType"  [attr-defined]
    # But actually it is there.
    types.CellType,  # type: ignore[attr-defined]
    types.ModuleType,
    types.MappingProxyType,
    types.SimpleNamespace,
)
_symbol_types: tuple[type, ...] = tuple()

_tmp_symbol_types = []
for _name, _attr in getmembers(types, isclass):
    if _name.startswith('_'):
        continue

    if _attr in _known_object_types:
        pass
    else:
        _tmp_symbol_types.append(_attr)

_symbol_types = tuple(_tmp_symbol_types)


@overload
def typeof(value: bool) -> Literal['boolean']:
    ...


@overload
def typeof(value: Number) -> Literal['number']:
    ...


@overload
def typeof(value: str) -> Literal['string']:
    ...


@overload
def typeof(value: Callable) -> Literal['function']:
    ...


@overload
def typeof(value: None) -> Literal['object']:
    ...


def typeof(value: Any) -> Literal['boolean', 'number', 'string', 'symbol', 'function', 'object']:
    """The simulator of `typeof` in JavaScript.

    JavaScript-side:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof#description

    Python-side:
    https://docs.python.org/3/library/types.html#standard-interpreter-types

    Precondition:

    | Types / Values                                                    | Result     | Assert By  |
    |-------------------------------------------------------------------|------------|------------|
    | bool (bool cannot have subclasses)                                | 'boolean'  | Type       |
    | numbers.Number, and its subclasses                                | 'number'   | Type       |
    | str, and its subclasses                                           | 'string'   | Type       |
    | NoneType, CellType, ModuleType, MappingProxyType, SimpleNamespace | 'object'   | Type       |
    | the other types in module types                                   | 'symbol'   | Type       |
    | Callable                                                          | 'function' | Value      |
    | any others                                                        | 'object'   | [fallback] |

    Notes:

    The reason why `CellType`, `ModuleType`, `MappingProxyType` and `SimpleNamespace`
    are considered to be 'object', is that users can manually control its properties,
    and `MappingProxyType`, which is seen as `dict`, is like the literal style in
    JavaScript that defines object.
    """

    if isinstance(value, _boolean_types):
        return 'boolean'
    elif isinstance(value, _number_types):
        return 'number'
    elif isinstance(value, _string_types):
        return 'string'
    elif isinstance(value, _known_object_types):
        return 'object'
    elif isinstance(value, _symbol_types):
        return 'symbol'
    elif callable(value):
        return 'function'
    else:
        return 'object'


U = TypeVar('U')
S = TypeVar('S')


class Array(MutableSequence[_T], ABC, Generic[_T]):
    @staticmethod
    def is_array(value: Any) -> TypeGuard[MutableSequence[_T]]:
        return isinstance(value, MutableSequence) and not isinstance(value, str)

    @overload
    @staticmethod
    def from_(
        iterable: Iterable[_T], map_fn: Callable[[S, _T], U], self_arg: S, /
    ) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(
        iterable: Iterable[_T], map_fn: Callable[[S, _T, int], U], self_arg: S, /
    ) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[_T], /) -> MutableSequence[_T]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[_T], map_fn: Callable[[_T], U], /) -> MutableSequence[U]:
        ...

    @overload
    @staticmethod
    def from_(iterable: Iterable[_T], map_fn: Callable[[_T, int], U], /) -> MutableSequence[U]:
        ...

    # mypy: Overloaded function implementation does not accept all possible arguments of signature 5
    # pyright: 0 error, 0 warnings, 0 infos
    @staticmethod  # type: ignore[misc]
    def from_(
        iterable: Iterable[_T],
        map_fn: Optional[
            Union[
                Callable[[S, _T], U],
                Callable[[S, _T, int], U],
                Callable[[_T], U],
                Callable[[_T, int], U],
            ]
        ] = None,
        self_arg: Optional[S] = None,
        /,
    ) -> Any:
        if self_arg is not None:
            map_fn = cast(Optional[Union[Callable[[S, _T], U], Callable[[S, _T, int], U]]], map_fn)

            if map_fn is None:
                raise ValueError('`map_fn` cannot be None when `self_arg` is not None.')

            # https://docs.python.org/3/howto/descriptor.html#functions-and-methods
            bound_map_fn = cast(
                Union[Callable[[_T], U], Callable[[_T, int], U]],
                types.MethodType(map_fn, self_arg),
            )

            # bound method's signature will lost self argument
            param_count_without_self = len(signature(bound_map_fn).parameters)

            if param_count_without_self == 1:
                bound_map_fn = cast(Callable[[_T], U], bound_map_fn)

                return [bound_map_fn(e) for e in iterable]  # pylint: disable=not-callable

            else:
                bound_map_fn = cast(Callable[[_T, int], U], bound_map_fn)

                return [
                    bound_map_fn(e, i)  # pylint: disable=not-callable
                    for i, e in enumerate(iterable)
                ]

        else:
            map_fn = cast(Optional[Union[Callable[[_T], U], Callable[[_T, int], U]]], map_fn)

            if map_fn is None:
                return list(iterable)

            else:
                param_count = len(signature(map_fn).parameters)

                if param_count == 1:
                    map_fn = cast(Callable[[_T], U], map_fn)

                    return [map_fn(e) for e in iterable]

                else:
                    map_fn = cast(Callable[[_T, int], U], map_fn)

                    return [map_fn(e, i) for i, e in enumerate(iterable)]
