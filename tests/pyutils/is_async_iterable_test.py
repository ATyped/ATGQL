from typing import Any

from atgql.pyutils.identity_func import identity_func
from atgql.pyutils.is_async_iterable import is_async_iterable


def test_should_return_true_for_async_iterable():
    class AsyncIterable:
        def __aiter__(self):
            raise Exception("Shouldn't be executed")

        async def __anext__(self):
            raise Exception("Shouldn't be executed")

    async_iterable = AsyncIterable()
    assert is_async_iterable(async_iterable) is True

    async def async_generator_func() -> Any:
        yield

    assert is_async_iterable(async_generator_func()) is True
    assert is_async_iterable(async_generator_func) is False


def test_should_return_false_for_all_other_values():
    assert is_async_iterable(None) is False

    assert is_async_iterable('ABC') is False
    assert is_async_iterable('0') is False
    assert is_async_iterable('') is False

    assert is_async_iterable([]) is False
    assert is_async_iterable([1]) is False
    assert is_async_iterable({}) is False
    assert is_async_iterable({'iterable': True}) is False

    non_async_iterable: Any = iter([])
    assert is_async_iterable(non_async_iterable) is False

    def generator_func():
        yield

    assert is_async_iterable(generator_func) is False

    class InvalidAsyncIterable:
        def __aiter__(self):
            raise Exception("Shouldn't be executed")

        __anext__ = {'next': identity_func}

    invalid_async_iterable = InvalidAsyncIterable()
    # It should be `assert is_async_iterable(invalid_async_iterable) is False`,
    # but runtime_checkable() will check only the presence of the required methods,
    # not their type signatures!
    # see https://docs.python.org/3/library/typing.html#typing.runtime_checkable
    assert is_async_iterable(invalid_async_iterable) is True
