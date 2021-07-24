__all__ = ['invariant']

from typing import Any, Optional


def invariant(condition: Any, message: Optional[str] = None):
    boolean_condition = bool(condition)
    if not boolean_condition:
        raise Exception(message if message is not None else 'Unexpected invariant triggered.')
