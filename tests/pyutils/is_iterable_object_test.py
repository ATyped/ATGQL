from typing import Any

from atgql.pyutils.is_iterable_object import is_iterable_object


def test_should_return_true_for_collections():
    assert is_iterable_object([]) is True
    assert is_iterable_object([1]) is True

    assert is_iterable_object('ABC') is True

    def get_arguments(*args) -> Any:
        return args

    assert is_iterable_object(get_arguments()) is True
