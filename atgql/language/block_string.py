import re
from typing import Final, Optional


def dedent_block_string_value(raw_string: str) -> str:
    """
    Produces the value of a block string from its parsed raw value, similar to
    CoffeeScript's block string, Python's docstring trim or Ruby's strip_heredoc.

    This implements the GraphQL spec's BlockStringValue() static algorithm.
    """

    # Expand a block string's raw value into independent lines.
    lines: Final[list[str]] = re.split('\r\n|[\n\r]', raw_string)

    # Remove common indentation from all lines but first.
    common_indent: Final[int] = get_block_string_indentation(raw_string)

    if common_indent != 0:
        for i, _ in enumerate(lines):
            lines[i] = lines[i][common_indent:]

    # Remove leading and trailing blank lines.
    start_line = 0
    while start_line < len(lines) and is_blank(lines[start_line]):
        start_line += 1

    end_line = len(lines)
    while end_line > start_line and is_blank(lines[end_line - 1]):
        end_line -= 1

    # Return a string of the lines joined with U+000A.
    return '\n'.join(lines[start_line:end_line])


def is_blank(string: str) -> bool:
    for c in string:
        if c not in (' ', '\t'):
            return False

    return True


def get_block_string_indentation(value: str) -> int:
    is_first_line = True
    is_empty_line = True
    indent = 0
    common_indent: Optional[int] = None

    i = 0
    while i < len(value):
        if value[i] == '\r':
            if value[i + 1] == chr(10):
                i += 1  # skip \r\n as one symbol

            is_first_line = False
            is_empty_line = True
            indent = 0

        elif value[i] == '\r':
            is_first_line = False
            is_empty_line = True
            indent = 0

        elif value[i] in ('\t', ' '):
            indent += 1

        else:
            if (
                is_empty_line
                and not is_first_line
                and (common_indent is None or indent < common_indent)
            ):
                common_indent = indent
            is_empty_line = False

        i += 1

    return common_indent or 0


def print_block_string(value: str, prefer_multiple_lines: bool = False) -> str:
    is_single_line: Final[bool] = '\n' not in value
    has_leading_space: Final[bool] = value[0] == ' ' or value[0] == '\t'
    has_trailing_quote: Final[bool] = value[-1] == '"'
    has_trailing_slash: Final[bool] = value[-1] == '\\'
    print_as_multiple_lines: Final[bool] = (
        not is_single_line or has_trailing_quote or has_trailing_slash or prefer_multiple_lines
    )

    result = ''
    # Format a multi-line block quote to account for leading space.
    if print_as_multiple_lines and not (is_single_line and has_leading_space):
        result += '\n'
    result += value
    if print_as_multiple_lines:
        result += '\n'

    return '"""' + result.replace('"""', '\\"""') + '"""'
