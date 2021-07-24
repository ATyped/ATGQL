__all__ = ['promise_reduce']

from collections.abc import Iterable
from typing import Callable, TypeVar, cast

from atgql.pyutils.is_promise import is_promise
from atgql.pyutils.promise_or_value import PromiseOrValue
from atgql.shims import Promise

T = TypeVar('T')
U = TypeVar('U')


async def promise_then(
    promise: Promise[U],
    then: Callable[[U], PromiseOrValue[U]],
) -> U:
    resolved = await promise
    accumulated = then(resolved)

    if is_promise(accumulated):
        accumulated = await accumulated
    else:
        accumulated = cast(U, accumulated)

    return accumulated


def bind_current_value(
    callback_fn: Callable[[U, T], PromiseOrValue[U]], current_value: T
) -> Callable[[U], PromiseOrValue[U]]:
    return lambda resolved: callback_fn(resolved, current_value)


def promise_reduce(
    values: Iterable[T],
    callback_fn: Callable[[U, T], U],
    initial_value: PromiseOrValue[U],
) -> PromiseOrValue[U]:
    accumulator = initial_value
    for value in values:
        if is_promise(accumulator):
            accumulator = promise_then(
                # FIXME: there shouldn't need typecast, it's a bug of mypy
                cast(Promise[U], accumulator),
                bind_current_value(callback_fn, value),
            )
        else:
            accumulator = callback_fn(cast(U, accumulator), value)
    return accumulator
