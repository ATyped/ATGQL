from itertools import takewhile


def natural_compare(a_str: str, b_str: str) -> int:
    """
    Returns a number indicating whether a reference string comes before, or after,
    or is the same as the given string in natural sort order.

    See: https://en.wikipedia.org/wiki/Natural_sort_order
    """

    a_idx, b_idx = 0, 0

    while a_idx < len(a_str) and b_idx < len(b_str):
        a_char = a_str[a_idx]
        b_char = b_str[b_idx]

        if a_char.isdigit() and b_char.isdigit():
            a_num_str = str(''.join(takewhile(lambda c: c.isdigit(), a_str[a_idx:])))
            a_idx += len(a_num_str)
            a_num = int(a_num_str)

            b_num_str = str(''.join(takewhile(lambda c: c.isdigit(), b_str[b_idx:])))
            b_idx += len(b_num_str)
            b_num = int(b_num_str)

            if a_num < b_num:
                return -1

            if a_num > b_num:
                return 1

        else:
            if a_char < b_char:
                return -1
            if a_char > b_char:
                return 1

            a_idx += 1
            b_idx += 1

    return len(a_str) - len(b_str)
