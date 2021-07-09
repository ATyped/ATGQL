from typing import Final, Optional, Sequence, Union, cast, overload

MAX_SUGGESTIONS: Final[int] = 5


@overload
def did_you_mean(suggestions: Sequence[str], /) -> str:
    ...


@overload
def did_you_mean(sub_message: str, suggestions: Sequence[str], /) -> str:
    ...


def did_you_mean(
    first_arg: Union[str, Sequence[str]], second_arg: Optional[Sequence[str]] = None, /
) -> str:
    sub_message, suggestions_arg = (
        (cast(str, first_arg), second_arg) if second_arg is not None else (None, first_arg)
    )

    message = ' Did you mean '
    if sub_message is not None:
        message += f'{sub_message} '

    suggestions: Final[list[str]] = list(map(lambda x: f'"{x}"', suggestions_arg))
    len_suggestions = len(suggestions)
    if len_suggestions == 0:
        return ''
    elif len_suggestions == 1:
        return f'{message}{suggestions[0]}?'
    elif len_suggestions == 2:
        return f'{message}{suggestions[0]} or {suggestions[1]}?'

    selected = suggestions[:MAX_SUGGESTIONS]
    last_item: Final[str] = selected.pop()
    return f'{message}{", ".join(selected)}, or {last_item}?'
