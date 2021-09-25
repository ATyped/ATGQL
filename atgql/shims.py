__all__ = ['Promise', 'typeof', 'Array']


import types
from abc import ABC
from collections.abc import Awaitable, Callable, Iterable, MutableSequence
from inspect import signature
from math import inf
from numbers import Number
from typing import Any, Generic, Literal, Optional, TypeVar, Union, cast, overload

from typing_extensions import TypeGuard

_T = TypeVar('_T')

Promise = Awaitable[_T]


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


@overload
def typeof(value: Any) -> Literal['boolean', 'number', 'string', 'function', 'object']:
    ...


def typeof(value: Any) -> Literal['boolean', 'number', 'string', 'function', 'object']:
    """The simulator of `typeof` in JavaScript.

    JavaScript-side:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/typeof#description

    Python-side:
    https://docs.python.org/3/library/types.html#standard-interpreter-types
    """

    if isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, Number):
        return 'number'
    elif isinstance(value, str):
        return 'string'
    elif callable(value):
        return 'function'
    else:
        return 'object'


U = TypeVar('U')
S = TypeVar('S')


class Array(Generic[_T]):
    @staticmethod
    def is_array(value: Union[MutableSequence[_T], Any]) -> TypeGuard[MutableSequence[_T]]:
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

    @overload
    @staticmethod
    def splice(this: MutableSequence[_T], start: Union[int, float], /) -> MutableSequence[_T]:
        ...

    @overload
    @staticmethod
    def splice(
        this: MutableSequence[_T], start: Union[int, float], delete_count: Union[int, float], /
    ) -> MutableSequence[_T]:
        ...

    @overload
    @staticmethod
    def splice(
        this: MutableSequence[_T],
        start: Union[int, float],
        delete_count: Union[int, float],
        *items: _T,
    ) -> MutableSequence[_T]:
        ...

    # mypy: Overloaded function implementation does not accept all possible arguments of signature 3
    # pyright: 0 error, 0 warnings, 0 infos
    @staticmethod  # type: ignore[misc]
    def splice(this: MutableSequence[_T], *args: Any) -> MutableSequence[_T]:
        start = args[0]
        if isinstance(start, float):
            start = round(start) if start != -inf else 0
        delete_count = args[1] if len(args) >= 2 else None
        if isinstance(delete_count, float):
            delete_count = round(delete_count)
        items: Iterable[_T] = args[2:] if len(args) >= 3 else []

        # If greater than the length of the array, start will be set to the length of the array.
        # If negative, it will begin that many elements from the end of the array.
        # If start is negative infinity, it will begin from index 0.
        self_length = len(this)
        start = min(self_length, start)

        # If delete_count is omitted, or if its value is equal to or larger than len(self) - start,
        # then all the elements from start to the end of the array will be deleted.
        # If deleteCount is 0 or negative, no elements are removed.
        length_to_be_processed = self_length - start
        if delete_count is None or delete_count >= length_to_be_processed:
            delete_count = length_to_be_processed
        elif delete_count < 0:
            delete_count = 0

        end = start + delete_count
        removed = this[start:end]
        this[start:end] = items

        return removed


class UndefinedType:
    ...


undefined = UndefinedType()


class Object:
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        return setattr(self, key, value)
