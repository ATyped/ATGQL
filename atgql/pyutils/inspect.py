# Adapted from graphql-python/graphql-core
# https://github.com/graphql-python/graphql-core/blob/v3.1.5/src/graphql/pyutils/inspect.py
#
# Origin file is licensed by MIT License:
# https://github.com/graphql-python/graphql-core/blob/v3.1.5/LICENSE

from inspect import (
    isasyncgen,
    isasyncgenfunction,
    isclass,
    iscoroutine,
    iscoroutinefunction,
    isfunction,
    isgenerator,
    isgeneratorfunction,
    ismethod,
)
from typing import Any, Final, Sequence

MAX_RECURSIVE_DEPTH: Final[int] = 2
MAX_STR_SIZE: Final[int] = 240
MAX_ARRAY_LENGTH: Final[int] = 10


def inspect(value: Any) -> str:
    """Used to print values in error messages."""

    return format_value(value, [])


def format_value(value: Any, seen_values: Sequence[Any]) -> str:
    if value is None or isinstance(value, (bool, float, complex)):
        return repr(value)
    if isinstance(value, (int, str, bytes, bytearray)):
        return trunc_str(repr(value))
    if len(seen_values) < MAX_RECURSIVE_DEPTH and value not in seen_values:
        # recursively inspect collections
        if isinstance(value, (list, tuple, dict, set, frozenset)):
            if not value:
                return repr(value)
            seen_values = [*seen_values, value]
            if isinstance(value, list):
                items = value
            elif isinstance(value, dict):
                items = list(value.items())
            else:
                items = list(value)
            items = trunc_list(items)
            if isinstance(value, dict):
                s = ', '.join(
                    '...'
                    if v is Ellipsis
                    else format_value(v[0], seen_values) + ': ' + format_value(v[1], seen_values)
                    for v in items
                )
            else:
                s = ', '.join(
                    '...' if v is Ellipsis else format_value(v, seen_values) for v in items
                )
            if isinstance(value, tuple):
                if len(items) == 1:
                    return f'({s},)'
                return f'({s})'
            if isinstance(value, (dict, set)):
                return '{' + s + '}'
            if isinstance(value, frozenset):
                return f'frozenset({{{s}}})'
            return f'[{s}]'
    else:
        # handle collections that are nested too deep
        if isinstance(value, (list, tuple, dict, set, frozenset)):
            if not value:
                return repr(value)
            if isinstance(value, list):
                return '[...]'
            if isinstance(value, tuple):
                return '(...)'
            if isinstance(value, dict):
                return '{...}'
            if isinstance(value, set):
                return 'set(...)'
            return 'frozenset(...)'
    if isinstance(value, Exception):
        type_ = 'exception'
        value = type(value)
    elif isclass(value):
        type_ = 'exception class' if issubclass(value, Exception) else 'class'
    elif ismethod(value):
        type_ = 'method'
    elif iscoroutinefunction(value):
        type_ = 'coroutine function'
    elif isasyncgenfunction(value):
        type_ = 'async generator function'
    elif isgeneratorfunction(value):
        type_ = 'generator function'
    elif isfunction(value):
        type_ = 'function'
    elif iscoroutine(value):
        type_ = 'coroutine'
    elif isasyncgen(value):
        type_ = 'async generator'
    elif isgenerator(value):
        type_ = 'generator'
    else:
        return repr(value)

    try:
        name = value.__name__
        if not name or '<' in name or '>' in name:
            raise AttributeError
    except AttributeError:
        return f'<{type_}>'
    else:
        return f'<{type_} {name}>'


def trunc_str(s: str) -> str:
    """Truncate strings to maximum length."""

    if len(s) > MAX_STR_SIZE:
        i = max(0, (MAX_STR_SIZE - 3) // 2)
        j = max(0, MAX_STR_SIZE - 3 - i)
        s = s[:i] + '...' + s[-j:]
    return s


def trunc_list(s: list) -> list:
    """Truncate lists to maximum length."""

    if len(s) > MAX_ARRAY_LENGTH:
        i = MAX_ARRAY_LENGTH // 2
        j = i - 1
        s = s[:i] + [Ellipsis] + s[-j:]
    return s
