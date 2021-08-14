__all__ = ['suggestion_list']

from collections.abc import Sequence
from functools import cmp_to_key
from math import floor
from typing import Final, Optional

from atgql.pyutils.natural_compare import natural_compare


def suggestion_list(input_: str, options: Sequence[str]) -> list[str]:
    """
    Given an invalid input string and a list of valid options, returns a filtered
    list of valid options sorted based on their similarity with the input.
    """

    options_by_distance: dict[str, int] = {}
    lexical_distance = LexicalDistance(input_)

    threshold = floor(len(input_) * 0.4) + 1
    for option in options:
        distance = lexical_distance.measure(option, threshold)
        if distance is not None:
            options_by_distance[option] = distance

    def comparer(a: str, b: str) -> int:
        distance_diff = options_by_distance[a] - options_by_distance[b]
        return distance_diff if distance_diff != 0 else natural_compare(a, b)

    return sorted(options_by_distance.keys(), key=cmp_to_key(comparer))


class LexicalDistance:
    """Computes the lexical distance between strings A and B.

    The "distance" between two strings is given by counting the minimum number
    of edits needed to transform string A into string B. An edit can be an
    insertion, deletion, or substitution of a single character, or a swap of two
    adjacent characters.

    Includes a custom alteration from Damerau-Levenshtein to treat case changes
    as a single edit which helps identify mis-cased values with an edit distance
    of 1.

    This distance can be useful for detecting typos in input or sorting
    """

    _input: str
    _input_lower_case: str
    _input_array: list[int]
    _rows: tuple[list[int], list[int], list[int]]

    def __init__(self, input_: str) -> None:
        self._input = input_
        self._input_lower_case = input_.lower()
        self._input_array = string_to_array(self._input_lower_case)

        self._rows = (
            [0] * (len(input_) + 1),
            [0] * (len(input_) + 1),
            [0] * (len(input_) + 1),
        )

    def measure(self, option: str, threshold: int) -> Optional[int]:
        if self._input == option:
            return 0

        option_lower_case: Final[str] = option.lower()

        # Any case change counts as a single edit
        if self._input_lower_case == option_lower_case:
            return 1

        a = string_to_array(option_lower_case)
        b = self._input_array

        if len(a) < len(b):
            a, b = b, a
        a_length = len(a)
        b_length = len(b)

        rows = self._rows
        for j in range(b_length + 1):
            rows[0][j] = j

        for i in range(1, a_length + 1):
            up_row = rows[(i - 1) % 3]
            current_row = rows[i % 3]

            smallest_cell = current_row[0] = i
            for j in range(1, b_length + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1

                current_cell = min(
                    up_row[j] + 1,  # delete
                    current_row[j - 1] + 1,  # insert
                    up_row[j - 1] + cost,  # substitute
                )

                if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                    # transposition
                    double_diagonal_cell = rows[(i - 2) % 3][j - 2]
                    current_cell = min(current_cell, double_diagonal_cell + 1)

                if current_cell < smallest_cell:
                    smallest_cell = current_cell

                current_row[j] = current_cell

            # Early exit, since distance can't go smaller than smallest element of the previous row.
            if smallest_cell > threshold:
                return None

        distance = rows[a_length % 3][b_length]
        return distance if distance <= threshold else None


def string_to_array(str_: str) -> list[int]:
    return [ord(c) for c in str_]
