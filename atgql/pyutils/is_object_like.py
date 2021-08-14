__all__ = ['is_object_like']


from typing import Any

from typing_extensions import TypeGuard

from atgql.shims import typeof


def is_object_like(value: Any) -> TypeGuard[object]:
    """
    Return true if `value` is object-like. A value is object-like if it's not
    `None` and has a `typeof` result of "object".
    """

    return typeof(value) == 'object' and value is not None
