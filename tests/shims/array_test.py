from collections.abc import Iterator
from math import inf

import pytest

from atgql.shims import Array


def test_str_is_not_array():
    assert not Array.is_array('')
    assert not Array.is_array('hello, world')


def test_generator_is_not_array():
    def g() -> Iterator[int]:
        yield 1

    assert not Array.is_array(g())


def test_iterator_is_not_array():
    assert not Array.is_array(iter([]))


def test_iterable_is_not_array():
    assert not Array.is_array((1,))
    assert not Array.is_array({1: 2})


def test_list_instance_is_array():
    assert Array.is_array(list([]))
    assert Array.is_array(list([1, 2]))


def test_list_literal_is_array():
    assert Array.is_array([])
    assert Array.is_array([1, 2, 3])


def test_new_array_from_list_instance():
    raw = [1, 2, 3]
    copied = Array.from_(raw)
    assert id(copied) != id(raw)
    assert copied == raw


def test_from_is_shallow_copy():
    raw = [object()]
    copied = Array.from_(raw)
    assert id(copied) != id(raw)
    assert copied == raw
    assert id(copied[0]) == id(raw[0])  # pylint: disable=unsubscriptable-object


def test_from_do_transform_through_function_without_index():
    def transform(raw: int) -> float:
        return float(raw)

    assert Array.from_([1, 2, 3], transform) == [1.0, 2.0, 3.0]


def test_from_do_transform_through_function_with_index():
    def transform(raw: int, index: int):
        return raw * index

    assert Array.from_([1, 2, 3], transform) == [0, 2, 6]


def test_from_do_transform_through_unbound_method_without_index():
    class Transformer:
        def __init__(self, constant: int):
            self.constant = constant

        def do_job(self, _: int) -> int:
            return self.constant

    assert Array.from_([1, 2, 3], Transformer.do_job, Transformer(1)) == [1, 1, 1]


def test_from_do_transform_through_unbound_method_with_index():
    class Transformer:
        def __init__(self, constant: int):
            self.constant = constant

        def do_job(self, raw: int, index: int) -> int:
            return self.constant * raw * index

    assert Array.from_([1, 2, 3], Transformer.do_job, Transformer(2)) == [0, 4, 12]


def test_from_wrong_invocation():
    with pytest.raises(ValueError, match='`map_fn` cannot be None when `self_arg` is not None.'):
        Array.from_([], None, object())  # type: ignore[call-overload]


def test_splice_remove_zero_elements_before_index_2_and_insert_drum():
    my_fish = ['angel', 'clown', 'mandarin', 'sturgeon']

    assert Array.splice(my_fish, 2, 0, 'drum') == []
    assert my_fish == ['angel', 'clown', 'drum', 'mandarin', 'sturgeon']


def test_splice_remove_zero_elements_before_index_2_and_insert_drum_and_guitar():
    my_fish = ['angel', 'clown', 'mandarin', 'sturgeon']

    assert Array.splice(my_fish, 2, 0, 'drum', 'guitar') == []
    assert my_fish == ['angel', 'clown', 'drum', 'guitar', 'mandarin', 'sturgeon']


def test_splice_remove_1_element_at_index_3():
    my_fish = ['angel', 'clown', 'drum', 'mandarin', 'sturgeon']

    assert Array.splice(my_fish, 3, 1) == ['mandarin']
    assert my_fish == ['angel', 'clown', 'drum', 'sturgeon']


def test_splice_remove_1_element_at_index_2_and_insert_trumpet():
    my_fish = ['angel', 'clown', 'drum', 'sturgeon']

    assert Array.splice(my_fish, 2, 1, 'trumpet') == ['drum']
    assert my_fish == ['angel', 'clown', 'trumpet', 'sturgeon']


def test_splice_remove_2_elements_from_index_0_and_insert_parrot_anemone_blue():
    my_fish = ['angel', 'clown', 'trumpet', 'sturgeon']

    assert Array.splice(my_fish, 0, 2, 'parrot', 'anemone', 'blue') == ['angel', 'clown']
    assert my_fish == ['parrot', 'anemone', 'blue', 'trumpet', 'sturgeon']


def test_splice_remove_2_elements_starting_from_index_2():
    my_fish = ['parrot', 'anemone', 'blue', 'trumpet', 'sturgeon']

    assert Array.splice(my_fish, 2, 2) == ['blue', 'trumpet']
    assert my_fish == ['parrot', 'anemone', 'sturgeon']


def test_splice_remove_1_element_from_index_negative_2():
    my_fish = ['angel', 'clown', 'mandarin', 'sturgeon']

    assert Array.splice(my_fish, -2, 1) == ['mandarin']
    assert my_fish == ['angel', 'clown', 'sturgeon']


def test_splice_remove_all_elements_starting_from_index_2():
    my_fish = ['angel', 'clown', 'mandarin', 'sturgeon']

    assert Array.splice(my_fish, 2) == ['mandarin', 'sturgeon']
    assert my_fish == ['angel', 'clown']


def test_splice_start_greater_than_length():
    alphabet = ['a', 'b', 'c']

    assert Array.splice(alphabet, 10000, 1) == []
    assert alphabet == ['a', 'b', 'c']


def test_splice_start_from_negative_inf():
    alphabet = ['a', 'b', 'c']

    assert Array.splice(alphabet, -inf, 1) == ['a']
    assert alphabet == ['b', 'c']


def test_splice_delete_count_less_than_zero():
    alphabet = ['a', 'b', 'c']

    assert Array.splice(alphabet, 0, -1) == []
    assert alphabet == ['a', 'b', 'c']
