__all__ = ['Maybe']

from typing import Optional, TypeVar

T = TypeVar('T')

Maybe = Optional[T]
