from collections.abc import Awaitable
from typing import TypeVar

T = TypeVar('T')

Promise = Awaitable[T]
