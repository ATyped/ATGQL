import re

from atgql.pyutils.identity_func import identity_func
from atgql.pyutils.is_object_like import is_object_like


def test_should_return_true_for_objects():
    assert is_object_like({}) is True
    assert is_object_like(object()) is True
    assert is_object_like(re.compile('a')) is True
    assert is_object_like([]) is True


def test_should_return_false_for_non_objects():
    assert is_object_like(None) is False
    assert is_object_like(True) is False
    assert is_object_like('') is False
    assert is_object_like(identity_func) is False
