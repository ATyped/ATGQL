from typing import Any

from typing_extensions import TypeGuard


def is_object_like(value: Any) -> TypeGuard[object]:
    return isinstance(value, object)  # will always return True
