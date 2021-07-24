__all__ = ['dev_assert']

from typing import Any, Final


def dev_assert(condition: Any, message: str) -> None:
    boolean_condition: Final[bool] = bool(condition)

    if not boolean_condition:
        raise Exception(message)
