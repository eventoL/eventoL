import unittest

import autofixture
import mock
from django import forms

from manager.models import EventUser, Organizer
from manager.templatetags import filters


class TestTagFilters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.admin = autofixture.create_one('auth.User', field_values={'is_superuser': True, 'is_staff': True})
        cls.user = autofixture.create_one('auth.User', field_values={'is_superuser': False, 'is_staff': False})
        cls.event = autofixture.create_one('manager.Event')

    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
        cls.user.delete()
        cls.event.delete()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def deleteAllFromModel(self, model):
        models = model.objects.all()
        for model in models:
            if model.id:
                model.delete()

    def genetateEventUser(self):
        self.event_user = autofixture.create_one('manager.EventUser', {'user': self.user, 'event': self.event})

    def generateUserWithRol(self, model):
        self.user_with_rol = autofixture.create_one('manager.'+str(model.__name__), {'event_user': self.event_user})

    def test_addcss_call_field_as_widget(self):
        field = mock.Mock()
        filters.addcss(field, 'btn')
        self.assertTrue(field.as_widget.called)

    def test_addcss_call_field_as_widget_with_correct_params(self):
        field = mock.Mock()
        filters.addcss(field, 'btn')
        field.as_widget.assert_called_with(attrs={"class": 'btn'})

    def test_if_widget_is_instance_of_checkboxinput_is_checkbox(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = forms.CheckboxInput()
        self.assertTrue(filters.is_checkbox(boundfield))

    def test_if_widget_is_instance_of_checkboxselectmultiple_is_checkbox(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = forms.CheckboxSelectMultiple()
        self.assertTrue(filters.is_checkbox(boundfield))

    def test_if_widget_not_is_instance_of_checkboxselectmultiple_or_checkboxinput_not_is_checkbox(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = mock.Mock()
        self.assertFalse(filters.is_checkbox(boundfield))

    def test_if_widget_is_instance_of_datetimeinput_is_datetime(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = forms.DateTimeInput()
        self.assertTrue(filters.is_datetime(boundfield))

    def test_if_widget_not_is_instance_of_datetimeinput_not_is_datetime(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = mock.Mock()
        self.assertFalse(filters.is_datetime(boundfield))

    def test_if_widget_is_instance_of_fileinput_is_fileinput(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = forms.FileInput()
        self.assertTrue(filters.is_fileinput(boundfield))

    def test_if_widget_not_is_instance_of_fileinput_not_is_fileinput(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = mock.Mock()
        self.assertFalse(filters.is_fileinput(boundfield))

    def test_if_widget_is_instance_of_select_is_select(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = forms.Select()
        self.assertTrue(filters.is_select(boundfield))

    def test_if_widget_not_is_instance_of_select_not_is_select(self):
        boundfield = mock.Mock()
        boundfield.field = mock.Mock()
        boundfield.field.widget = mock.Mock()
        self.assertFalse(filters.is_select(boundfield))

    def test_if_number_is_odd_is_odd(self):
        self.assertTrue(filters.is_odd(1))

    def test_if_number_not_is_odd_is_odd(self):
        self.assertFalse(filters.is_odd(2))

    def test_if_not_eventuser_is_registered_return_false(self):
        self.assertFalse(filters.is_registered(self.user, self.event.slug))

    def test_if_eventuser_is_registered_return_true(self):
        self.genetateEventUser()
        self.assertTrue(filters.is_registered(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)

    def test_if_not_eventuser_is_intaller_return_false(self):
        self.assertFalse(filters.is_installer(self.user, self.event.slug))

    def test_if_eventuser_and_not_is_installer_is_installer_return_false(self):
        self.genetateEventUser()
        self.assertFalse(filters.is_installer(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)

    def test_if_organizer_and_not_is_installer_is_installer_return_true(self):
        with mock.patch('manager.templatetags.filters.is_organizer') as is_organizer:
            is_organizer.return_value = True
            self.assertTrue(filters.is_installer(self.user, self.event.slug))

    def test_if_not_eventuser_is_collaborator_return_false(self):
        self.assertFalse(filters.is_collaborator(self.user, self.event.slug))

    def test_if_eventuser_and_not_is_collaborator_is_collaborator_return_false(self):
        self.genetateEventUser()
        self.assertFalse(filters.is_collaborator(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)

    def test_if_organizer_and_not_is_collaborator_is_collaborator_return_true(self):
        self.genetateEventUser()
        self.generateUserWithRol(Organizer)
        self.assertTrue(filters.is_collaborator(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)
        self.deleteAllFromModel(Organizer)

    def test_if_not_eventuser_is_organizer_return_false(self):
        self.assertFalse(filters.is_organizer(self.user, self.event.slug))

    def test_if_eventuser_and_not_is_organizer_is_organizer_return_false(self):
        self.genetateEventUser()
        self.assertFalse(filters.is_organizer(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)

    def test_if_organizer_is_organizer_return_true(self):
        self.genetateEventUser()
        self.generateUserWithRol(Organizer)
        self.assertTrue(filters.is_organizer(self.user, self.event.slug))
        self.deleteAllFromModel(EventUser)
        self.deleteAllFromModel(Organizer)

    def test_if_is_collaborator_and_not_has_perm_can_take_attendance_return_false(self):
        with mock.patch('manager.templatetags.filters.is_collaborator') as is_collaborator:
            is_collaborator.return_value = True
            self.user.has_perm = mock.Mock(return_value=False)
            self.assertFalse(filters.can_take_attendance(self.user, self.event.slug))

    def test_if_is_collaborator_and_has_perm_can_take_attendance_return_true(self):
        with mock.patch('manager.templatetags.filters.is_collaborator') as is_collaborator:
            is_collaborator.return_value = True
            self.user.has_perm = mock.Mock(return_value=True)
            self.assertTrue(filters.can_take_attendance(self.user, self.event.slug))

    def test_if_is_organizer_and_not_has_perm_can_take_attendance_return_false(self):
        with mock.patch('manager.templatetags.filters.is_organizer') as is_organizer:
            is_organizer.return_value = True
            self.assertFalse(filters.can_take_attendance(self.user, self.event.slug))
