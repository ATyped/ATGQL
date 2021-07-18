from collections.abc import Sequence
from typing import Union


def print_path_array(path: Sequence[Union[str, int]]) -> str:
    return ''.join(map(lambda key: f'[{key}]' if isinstance(key, int) else f'.{key}', path))
