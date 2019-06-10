# pylint: disable=invalid-name,line-too-long
from manager.views import count_by


def test_count_by_with_getter_function_with_error_should_return_empty_dict():
    def getter(element):
        raise Exception(element)
    array = [{'b': False}] * 4
    assert count_by(array, getter) == {}


def test_count_by_if_increment_function_has_error_should_return_empty_dict():
    def increment(element):
        raise Exception(element)
    array = [{'b': False}] * 4
    assert count_by(array, lambda n: n, increment=increment) == {}


def test_count_by_if_count_for_key_should_return_key_count():
    array = [{'b': 1}] * 4 + [{'b': 2}] * 4
    assert count_by(array, lambda el: el['b']) == {'1': 4, '2': 4}


def test_count_by_if_count_for_key_and_increment_with_value_should_return_key_count_incremented():
    array = [{'b': 1}] * 4 + [{'b': 2}] * 4
    assert count_by(array, lambda el: el['b'], lambda el: el['b']) == {'1': 4, '2': 8}


def test_count_by_use_with_list_should_return_count():
    array = [2] * 5 + [1] * 4
    assert count_by(array, lambda n: n) == {'1': 4, '2': 5}


def test_count_by_use_with_list_and_increment_with_value_should_return_count_incremented():
    array = [2] * 5 + [1] * 4
    assert count_by(array, lambda n: n, lambda n: n) == {'1': 4, '2': 10}
