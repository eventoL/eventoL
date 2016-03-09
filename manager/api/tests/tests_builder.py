import mock
import unittest
from api.rest.builder import ViewSetBuilder
from django.contrib.auth.models import User
from django.forms import ModelForm
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.filters import DjangoFilterBackend


class TestViewSetBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class UserSerializer(HyperlinkedModelSerializer):
            class Meta:
                model = User
                fields = ('url', 'username', 'email', 'is_staff')

        class UserForm(ModelForm):
            class Meta:
                model = User
                fields = ('username', 'email', 'is_staff')

        class UserWithFilter():
            @classmethod
            def for_filter(cls):
                return ('username', 'email', 'is_staff')

        cls.serializer = UserSerializer
        cls.form = UserForm
        cls.user_with_filter = UserWithFilter
        cls.user_fields = User._meta.get_all_field_names()

    def setUp(self):
        self.viewset = None
        self.builder = None
        self.generate_builder(User)

    def generate_builder(self, model, form=None, serializer=None, build=False):
        self.builder = ViewSetBuilder(model, form, serializer)
        if build:
            self.viewset = self.builder.build()

    def test_defult_setting(self):
        self.assertEqual(self.builder.cls, User)
        self.assertIsNone(self.builder.cls_form)
        self.assertIsNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.fields, self.user_fields)

    def test_setting_with_form(self):
        self.generate_builder(User, self.form)
        self.assertEqual(self.builder.cls, User)
        self.assertEqual(self.builder.cls_form, self.form)
        self.assertIsNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.fields, self.user_fields)

    def test_setting_with_serializer(self):
        self.generate_builder(User, serializer=self.serializer)
        self.assertEqual(self.builder.cls, User)
        self.assertEqual(self.builder.cls_serializer, self.serializer)
        self.assertIsNone(self.builder.cls_form)
        self.assertEqual(self.builder.fields, self.user_fields)

    def test_setting_with_form_and_serializer(self):
        self.generate_builder(User, self.form, self.serializer)
        self.assertEqual(self.builder.cls, User)
        self.assertEqual(self.builder.cls_serializer, self.serializer)
        self.assertEqual(self.builder.cls_form, self.form)
        self.assertEqual(self.builder.fields, self.user_fields)

    def test_setting_with_filter_in_model(self):
        self.generate_builder(self.user_with_filter)
        self.assertEqual(self.builder.cls, self.user_with_filter)
        self.assertIsNone(self.builder.cls_form)
        self.assertIsNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.fields, self.user_with_filter.for_filter())

    def test_check_viewset_is_class(self):
        self.generate_builder(User, build=True)
        self.assertIsInstance(type(self.viewset), type)

    def test_default_serializer(self):
        self.generate_builder(User, build=True)
        self.assertIsNotNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.cls_serializer.Meta.model, User)

    def test_serializer_with_form(self):
        self.generate_builder(User, self.form, build=True)
        self.assertIsNotNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.cls_serializer.Meta.model, User)
        self.assertEqual(self.builder.cls_serializer.Meta.fields, self.form.Meta.fields)

    def test_serializer_with_serializer(self):
        self.generate_builder(User, serializer=self.serializer, build=True)
        self.assertIsNotNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.cls_serializer, self.serializer)

    def test_serializer_with_form_and_serializer(self):
        self.generate_builder(User, self.form, self.serializer, True)
        self.assertIsNotNone(self.builder.cls_serializer)
        self.assertEqual(self.builder.cls_serializer, self.serializer)

    def test_view_set_serializer_is_serializer(self):
        self.generate_builder(User, build=True)
        self.assertEqual(self.viewset.serializer_class, self.builder.cls_serializer)

    def test_viewset_queryset_is_objects_all(self):
        self.generate_builder(User, build=True)
        self.assertListEqual(list(self.viewset.queryset), list(User.objects.all()))

    def test_viewset_filter_backents(self):
        self.generate_builder(User, build=True)
        self.assertEqual(self.viewset.filter_backends, (DjangoFilterBackend,))

    def test_viewset_filter_fields_in_default_building(self):
        self.generate_builder(User, build=True)
        self.assertEqual(self.viewset.filter_fields, self.user_fields)

    def test_viewset_filter_fields_with_filter(self):
        self.user_with_filter.objects = mock.Mock()
        self.generate_builder(self.user_with_filter, build=True)
        self.assertEqual(self.viewset.filter_fields, self.user_with_filter.for_filter())

    def test_viewset_ordering_fields_is_all(self):
        self.generate_builder(User, build=True)
        self.assertEqual(self.viewset.ordering_fields, '__all__')

    def test_set_fields_check_status_before_build(self):
        user_filter_fields = ('username', 'email')
        self.builder.set_fields(user_filter_fields)
        self.assertEqual(self.builder.fields, user_filter_fields)

    def test_set_fields_check_status_after_build(self):
        user_filter_fields = ('username', 'email')
        self.builder.set_fields(user_filter_fields)
        self.viewset = self.builder.build()
        self.assertEqual(self.viewset.filter_fields, user_filter_fields)

if __name__ == '__main__':
    unittest.main()