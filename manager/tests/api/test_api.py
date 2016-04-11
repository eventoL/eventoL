import json
import unittest
import datetime
import autofixture
from django.test import Client
from manager.api.rest.reduces import basic_reduce
from rest_framework.test import APIClient


class ApiTest(unittest.TestCase):

    url_base = None
    filter_fields = None
    example = None
    model = None
    str_model = None
    fk_models = []

    @classmethod
    def setUpClass(cls):
        if cls is ApiTest:
            raise unittest.SkipTest("Skip ApiTest tests, it's a base test class")
        cls.client = Client()
        cls.api_client = APIClient()
        cls.admin = autofixture.create_one('auth.User', field_values={
            'is_active': True, 'is_superuser': True, 'is_staff': True})
        cls.admin.set_password('secret')
        cls.admin.save()

    @classmethod
    def tearDownClass(cls):
        models = cls.model.objects.all()
        for model in models:
            if model.id:
                model.delete()

    def setUp(self):
        if self.fk_models:
            for fk_model in self.fk_models:
                autofixture.create_one(fk_model)
        self.example_generate = autofixture.create_one(self.str_model, field_values=self.example)
        self.client.login(username=self.admin.username, password='secret')
        self.api_client.login(username=self.admin.username, password='secret')

    def tearDown(self):
        self.client.logout()
        self.api_client.logout()
        if self.example_generate.id:
            self.example_generate.delete()
        models = filter(self.filter_model, self.model.objects.all())
        for model in models:
            if model.id:
                model.delete()

    def filter_model(self, model):
        return all(model._meta.get_field(key) == value for key, value in self.example.items())

    def verify_to_datetime(self, model, field):
        if isinstance(self.example[field], datetime.datetime):
            model[field] = datetime.datetime.strptime(model[field], "%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(self.example[field], datetime.date):
            model[field] = datetime.datetime.strptime(model[field], "%Y-%m-%d").date()

    def get_url(self, field):
        url = self.url_base + '?' + field + '='
        if isinstance(self.example[field], datetime.datetime):
            url += self.example[field].strftime('%Y-%m-%dT%H:%M:%S.%f')
            url = url.replace('T', '%20')
        elif isinstance(self.example[field], datetime.date):
            url += self.example[field].strftime("%Y-%m-%d")
        else:
            url += str(self.example[field])
        return url

    def get_reduce_url(self):
        return self.url_base + '?reduce=True'

    def get_model(self, models):
        for model in models:
            for key in self.example.keys():
                self.verify_to_datetime(model, key)
            if all(model[field] == value for field, value in self.example.items()):
                return model

    def test_get_url_base(self):
        response = self.client.get(self.url_base)
        self.assertEqual(response.status_code, 200)

    def test_if_logout_get_url_base_return_403(self):
        self.client.logout()
        self.api_client.logout()
        response = self.client.get(self.url_base)
        self.assertEqual(response.status_code, 403)


class ApiTestBuilder():

    def __init__(self, cls):
        class TestClass(cls, ApiTest):
            pass
        TestClass.__name__ = cls.__name__
        self.origin_cls = cls
        self.target_cls = TestClass
        self.suites = [self.suite_filter_fields_tests]
        self.get_filter_fields()

    def get_filter_fields(self):
        cls = self.target_cls
        if not cls.filter_fields:
            cls.filter_fields = cls.model.for_filter() if "for_filter" in dir(cls.model) else cls.model._meta.get_all_field_names()
            cls.filter_fields.pop(cls.filter_fields.index(u'id'))
            filter_fields = []
            for filter_field in cls.filter_fields:
                if filter_field in cls.example.keys() and not filter_field.endswith('_id'):
                    filter_fields.append(filter_field)
            cls.filter_fields = filter_fields

    def add_all_suites(self):
        for suite in self.suites:
            suite()

    def add_test(self, name, method):
        setattr(self.target_cls, name, method)

    def get_test_case(self):
        return self.target_cls

    def generate_filter_field_get_list(self, filter_field):
        def test(self):
            url = self.get_url(filter_field)
            response = self.client.get(url)
            self.assertTrue(len(json.loads(response.content)) > 0)
        return "test_filter_field_" + filter_field + '_object_in_this', test

    def generate_filter_field_get_object(self, filter_field):
        filter_fields = self.target_cls.filter_fields

        def test(self):
            url = self.get_url(filter_field)
            response = self.client.get(url)
            models = json.loads(response.content)
            model = self.get_model(models)
            for field in filter_fields:
                self.assertEqual(getattr(self.example_generate, field), model[field])
        return "test_filter_field_" + filter_field, test

    def generate_filter_field_check_filter(self, filter_field):
        def test(self):
            url = self.get_url(filter_field)
            response = self.client.get(url)
            models = json.loads(response.content)
            for model in models:
                self.verify_to_datetime(model, filter_field)
                self.assertEqual(model[filter_field], self.example[filter_field])
        return "test_filter_field_by_" + filter_field, test

    def reduce_tests(self):
        reduce = None
        if 'reduce' not in self.origin_cls.__dict__:
            def reduce(self, queryset):
                return basic_reduce(queryset)
        else:
            reduce = self.origin_cls.reduce
        self.target_cls.reduce = reduce

        def test(self):
            url = self.get_reduce_url()
            response = self.client.get(url)
            reduce = json.loads(response.content)
            self.assertEqual(reduce, self.reduce(self.model.objects.all()))
        return "test_reduce", test

    def reduce_tests_not_login(self):
        def test(self):
            self.client.logout()
            self.api_client.logout()
            url = self.get_reduce_url()
            response = self.client.get(url)
            reduce = json.loads(response.content)
            self.assertDictEqual(reduce, {u'detail': u'Authentication credentials were not provided.'})
        return "test_reduce_with_user_logout", test

    def suite_filter_fields_tests(self):
        for filter_field in self.target_cls.filter_fields:
            fields_tests = [self.generate_filter_field_get_object, self.generate_filter_field_get_list, self.generate_filter_field_check_filter]
            for field_test in fields_tests:
                test_name, test = field_test(filter_field)
                self.add_test(test_name, test)
        test_name, test = self.reduce_tests()
        self.add_test(test_name, test)
        test_name, test = self.reduce_tests_not_login()
        self.add_test(test_name, test)


def api_test():
    def class_rebuilder(cls):
        builder = ApiTestBuilder(cls)
        builder.add_all_suites()
        return builder.get_test_case()
    return class_rebuilder
