__all__ = ['PromiseOrValue']

from typing import TypeVar, Union

from atgql.shims import Promise

T = TypeVar('T')

PromiseOrValue = Union[Promise[T], T]
