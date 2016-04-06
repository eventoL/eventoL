import unittest
from manager.api.rest import reduces
import mock


class TestTagFilters(unittest.TestCase):

    def test_basic_reduce_call_count(self):
        queryset = mock.Mock()
        queryset.count = mock.Mock(return_value=3)
        reduces.basic_reduce(queryset)
        self.assertTrue(queryset.count.called)

    def test_basic_reduce_return(self):
        queryset = mock.Mock()
        queryset.count = mock.Mock(return_value=3)
        self.assertDictEqual(reduces.basic_reduce(queryset), {'total': 3})

    def test_count_if_return_two_of_four(self):
        lista = [{'a': True}]*3 + [{'a': False}]
        self.assertEqual(reduces.count_if(lista, {'a': True}), 3)

    def test_count_if_return_4_of_four(self):
        lista = [{'b': False}]*4
        self.assertEqual(reduces.count_if(lista, {'b': False}), 4)

    def test_count_if_error_in_condition_return_0_and_not_exception(self):
        lista = [{'a': True}]
        self.assertEqual(reduces.count_if(lista, 'ERROR'), 0)

    def test_count_by_if_getter_function_has_error_return_empty_dict(self):
        def getter(element):
            raise Exception(element)
        lista = [{'b': False}]*4
        self.assertDictEqual(reduces.count_by(lista, getter), {})

    def test_count_by_if_increment_function_has_error_return_empty_dict(self):
        def increment(element):
            raise Exception(element)
        lista = [{'b': False}]*4
        self.assertDictEqual(reduces.count_by(lista, lambda n: n, increment=increment), {})

    def test_count_by_if_count_for_key_return_key_count(self):
        lista = [{'b': 1}]*4+[{'b': 2}]*4
        self.assertDictEqual(reduces.count_by(lista, lambda el: el['b']), {1: 4, 2: 4})

    def test_count_by_if_count_for_key_and_increment_with_value_return_key_count_incremented(self):
        lista = [{'b': 1}]*4+[{'b': 2}]*4
        self.assertDictEqual(reduces.count_by(lista, lambda el: el['b'], lambda el: el['b']), {1: 4, 2: 8})

    def test_count_by_use_with_list_return_count(self):
        lista = [2]*5+[1]*4
        self.assertDictEqual(reduces.count_by(lista, lambda n: n), {1: 4, 2: 5})

    def test_count_by_use_with_list_and_increment_with_value_return_count_incremented(self):
        lista = [2]*5+[1]*4
        self.assertDictEqual(reduces.count_by(lista, lambda n: n, lambda n: n), {1: 4, 2: 10})

if __name__ == '__main__':
    unittest.main()