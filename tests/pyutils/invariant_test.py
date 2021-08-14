import pytest

from atgql.pyutils.invariant import invariant


def test_throws_on_false_conditions():
    with pytest.raises(Exception, match='Oops!'):
        invariant(False, 'Oops!')


def test_use_default_error_message():
    with pytest.raises(Exception, match='Unexpected invariant triggered.'):
        invariant(False)
