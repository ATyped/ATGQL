from typing import NoReturn, Optional, TypeVar, Union, overload

T = TypeVar('T')


@overload
def assert_not_none(value: None) -> NoReturn:
    ...


@overload
def assert_not_none(value: T) -> T:
    ...


def assert_not_none(value: Optional[T]) -> Union[NoReturn, T]:
    if value is None:
        raise Exception('Value should not be None.')
    return value
