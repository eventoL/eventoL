import unittest
from manager.views import count_by
from mock import Mock


class TestTagFilters(unittest.TestCase):

    def test_count_by_if_getter_function_has_error_return_empty_dict(self):
        def getter(element):
            raise Exception(element)
        lista = [{'b': False}] * 4
        self.assertDictEqual(count_by(lista, getter), {})

    def test_count_by_if_increment_function_has_error_return_empty_dict(self):
        def increment(element):
            raise Exception(element)
        lista = [{'b': False}] * 4
        self.assertDictEqual(count_by(lista, lambda n: n, increment=increment), {})

    def test_count_by_if_count_for_key_return_key_count(self):
        lista = [{'b': 1}] * 4 + [{'b': 2}] * 4
        self.assertDictEqual(count_by(lista, lambda el: el['b']), {1: 4, 2: 4})

    def test_count_by_if_count_for_key_and_increment_with_value_return_key_count_incremented(self):
        lista = [{'b': 1}] * 4 + [{'b': 2}] * 4
        self.assertDictEqual(count_by(lista, lambda el: el['b'], lambda el: el['b']), {1: 4, 2: 8})

    def test_count_by_use_with_list_return_count(self):
        lista = [2] * 5 + [1] * 4
        self.assertDictEqual(count_by(lista, lambda n: n), {1: 4, 2: 5})

    def test_count_by_use_with_list_and_increment_with_value_return_count_incremented(self):
        lista = [2] * 5 + [1] * 4
        self.assertDictEqual(count_by(lista, lambda n: n, lambda n: n), {1: 4, 2: 10})
