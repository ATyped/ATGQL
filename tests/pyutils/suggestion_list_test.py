from atgql.pyutils.suggestion_list import suggestion_list


def test_returns_when_input_is_empty():
    assert suggestion_list('', ['a']) == ['a']


def test_returns_empty_array_when_there_are_no_options():
    assert suggestion_list('input', []) == []


def test_returns_options_with_small_lexical_distance():
    assert suggestion_list('greenish', ['green']) == ['green']
    assert suggestion_list('green', ['greenish']) == ['greenish']


def test_rejects_options_with_small_lexical_distance():
    assert suggestion_list('aaaa', ['aaab']) == ['aaab']
    assert suggestion_list('aaaa', ['aabb']) == ['aabb']
    assert suggestion_list('aaaa', ['abbb']) == []

    assert suggestion_list('ab', ['ca']) == []


def test_returns_options_with_different_case():
    assert suggestion_list('verylongstring', ['VERYLONGSTRING']) == ['VERYLONGSTRING']

    assert suggestion_list('VERYLONGSTRING', ['verylongstring']) == ['verylongstring']

    assert suggestion_list('VERYLONGSTRING', ['VeryLongString']) == ['VeryLongString']


def test_returns_options_with_transpositions():
    assert suggestion_list('agr', ['arg']) == ['arg']
    assert suggestion_list('214365879', ['123456789']) == ['123456789']


def test_returns_options_sorted_based_on_lexical_distance():
    assert suggestion_list('abc', ['a', 'ab', 'abc']) == ['abc', 'ab', 'a']


def test_returns_options_with_same_lexical_distance_sorted_lexicographically():
    assert suggestion_list('a', ['az', 'ax', 'ay']) == ['ax', 'ay', 'az']
