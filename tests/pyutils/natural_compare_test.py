from atgql.pyutils.natural_compare import natural_compare


def test_handles_empty_strings():
    assert natural_compare('', '') == 0

    assert natural_compare('', 'a') == -1
    assert natural_compare('', '1') == -1

    assert natural_compare('a', '') == 1
    assert natural_compare('1', '') == 1


def test_handles_strings_of_different_length():
    assert natural_compare('A', 'A') == 0
    assert natural_compare('A1', 'A1') == 0

    assert natural_compare('A', 'AA') == -1
    assert natural_compare('A1', 'A1A') == -1

    assert natural_compare('AA', 'A') == 1
    assert natural_compare('A1A', 'A1') == 1


def test_handles_numbers():
    assert natural_compare('0', '0') == 0
    assert natural_compare('1', '1') == 0

    assert natural_compare('1', '2') == -1
    assert natural_compare('2', '1') == 1

    assert natural_compare('2', '11') == -1
    assert natural_compare('11', '2') == 1


def test_handles_numbers_with_leading_zeros():
    assert natural_compare('00', '00') == 0
    assert natural_compare('0', '00') == -1
    assert natural_compare('00', '0') == 1

    assert natural_compare('02', '11') == -1
    assert natural_compare('11', '02') == 1

    assert natural_compare('011', '200') == -1
    assert natural_compare('200', '011') == 1


def test_handles_numbers_embedded_into_names():
    assert natural_compare('a0a', 'a0a') == 0
    assert natural_compare('a0a', 'a9a') == -1
    assert natural_compare('a9a', 'a0a') == 1

    assert natural_compare('a00a', 'a00a') == 0
    assert natural_compare('a00a', 'a09a') == -1
    assert natural_compare('a09a', 'a00a') == 1

    assert natural_compare('a0a1', 'a0a1') == 0
    assert natural_compare('a0a1', 'a0a9') == -1
    assert natural_compare('a0a9', 'a0a1') == 1

    assert natural_compare('a10a11a', 'a10a11a') == 0
    assert natural_compare('a10a11a', 'a10a19a') == -1
    assert natural_compare('a10a19a', 'a10a11a') == 1

    assert natural_compare('a10a11a', 'a10a11a') == 0
    assert natural_compare('a10a11a', 'a10a11b') == -1
    assert natural_compare('a10a11b', 'a10a11a') == 1
