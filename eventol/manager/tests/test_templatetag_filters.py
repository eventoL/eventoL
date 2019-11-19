# pylint: disable=invalid-name,line-too-long,too-many-public-methods,
import json
import autofixture
import pytest

from django import forms
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from manager.templatetags import filters


# get_contact_url
def test_get_contact_url_with_type_1_should_return_same_url(mocker):
    url = 'http://url/'
    contact = mocker.Mock()
    contact.url = url
    contact.type.validate = '1'
    assert filters.get_contact_url(contact) == url


def test_get_contact_url_with_type_2_should_return_mailto_url(mocker):
    url = 'eventol@eventol.org'
    expectedUrl = 'mailto:{}'.format(url)
    contact = mocker.Mock()
    contact.url = url
    contact.type.validate = '2'
    assert filters.get_contact_url(contact) == expectedUrl


# get_schedule_size
@pytest.mark.parametrize('rooms, expected', [
    ([], 0 * 200),
    (['R'], 1 * 200),
    (['R'] * 2, 2 * 200),
    (['R'] * 3, 3 * 200),
])
def test_get_schedule_size_should_return_200_for_each_room(rooms, expected):
    assert filters.get_schedule_size(json.dumps(rooms)) == expected


# get_schedule_date
@pytest.mark.parametrize('dic, key, expected', [
    ({'key': json.dumps({'datestring': 1})}, 'key', 1),
    ({'key2': json.dumps({'datestring': 2})}, 'key2', 2),
])
def test_get_schedule_date_should_return_correct_element(dic, key, expected):
    assert filters.get_schedule_date(dic, key) == expected


# addcss
def test_addcss_should_call_field_as_widget(mocker):
    field = mocker.Mock()
    filters.addcss(field, 'btn')
    assert field.as_widget.called


def test_addcss_should_call_field_as_widget_with_correct_params(mocker):
    field = mocker.Mock()
    filters.addcss(field, 'btn')
    field.as_widget.assert_called_with(attrs={'class': 'btn'})


# is_checkbox
def test_is_checkbox_with_CheckboxInput_return_true(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = forms.CheckboxInput()
    assert filters.is_checkbox(boundfield)


def test_is_checkbox_with_CheckboxSelectMultiple_return_true(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = forms.CheckboxSelectMultiple()
    assert filters.is_checkbox(boundfield)


def test_is_checkbox_with_MockWidget_return_false(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = mocker.Mock()
    assert not filters.is_checkbox(boundfield)


# is_datetime
def test_is_datetime_with_DateTimeInput_should_return_true(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = forms.DateTimeInput()
    assert filters.is_datetime(boundfield)


def test_is_datetime_with_MockWidget_should_return_false(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = mocker.Mock()
    assert not filters.is_datetime(boundfield)


# is_fileinput
def test_is_fileinput_with_FileInput_should_return_true(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = forms.FileInput()
    assert filters.is_fileinput(boundfield)

def test_is_fileinput_with_MockWidget_should_return_false(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = mocker.Mock()
    assert not filters.is_fileinput(boundfield)


# is_select
def test_is_select_with_Select_should_return_true(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = forms.Select()
    assert filters.is_select(boundfield)

def test_is_select_with_MockWidget_should_return_false(mocker):
    boundfield = mocker.Mock()
    boundfield.field = mocker.Mock()
    boundfield.field.widget = mocker.Mock()
    assert not filters.is_select(boundfield)


# is_odd
def test_is_odd_with_odd_number_should_return_true():
    assert filters.is_odd(1)

def test_is_odd_with_not_odd_number_should_return_false():
    assert not filters.is_odd(2)


# is_registered
@pytest.mark.django_db
def test_is_registered_with_event_user_should_return_true(event_user1, event1):
    assert filters.is_registered(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_registered_with_not_event_user_should_return_false(event_user1, event2):
    assert not filters.is_registered(event_user1.user, event2.event_slug)


# is_registered_any_way
@pytest.mark.django_db
def test_is_registered_any_way_with_is_attendee_true_should_return_true(mocker, user1, event1):
    mock_is_attendee = mocker.patch('manager.templatetags.filters.is_attendee')
    mock_is_registered = mocker.patch('manager.templatetags.filters.is_registered')
    mock_is_attendee.return_value = True
    mock_is_registered.return_value = False
    assert filters.is_registered_any_way(user1, event1.event_slug)
    assert mock_is_attendee.called
    assert not mock_is_registered.called
    mock_is_attendee.assert_called_once_with(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_registered_any_way_with_is_attendee_false_and_is_registered_true_should_return_true(mocker, user1, event1):
    mock_is_attendee = mocker.patch('manager.templatetags.filters.is_attendee')
    mock_is_registered = mocker.patch('manager.templatetags.filters.is_registered')
    mock_is_attendee.return_value = False
    mock_is_registered.return_value = True
    assert filters.is_registered_any_way(user1, event1.event_slug)
    assert mock_is_attendee.called
    assert mock_is_registered.called
    mock_is_attendee.assert_called_once_with(user1, event1.event_slug)
    mock_is_registered.assert_called_once_with(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_registered_any_way_with_is_attendee_false_and_is_registered_false_should_return_false(mocker, user1, event1):
    mock_is_attendee = mocker.patch('manager.templatetags.filters.is_attendee')
    mock_is_registered = mocker.patch('manager.templatetags.filters.is_registered')
    mock_is_attendee.return_value = False
    mock_is_registered.return_value = False
    assert not filters.is_registered_any_way(user1, event1.event_slug)
    assert mock_is_attendee.called
    assert mock_is_registered.called
    mock_is_attendee.assert_called_once_with(user1, event1.event_slug)
    mock_is_registered.assert_called_once_with(user1, event1.event_slug)


# is_installer
@pytest.mark.django_db
def test_is_installer_with_not_eventuser_should_return_false(user1, event1):
    assert not filters.is_installer(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_eventuser_not_installer_should_return_false(event_user1, event1):
    assert not filters.is_installer(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_installer_from_another_event_should_return_false(installer2, event1):
    assert not filters.is_installer(installer2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_installer_should_return_true(installer1, event1):
    assert filters.is_installer(installer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_organizer_should_return_true(mocker, organizer1, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = True
    assert filters.is_installer(organizer1.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_organizer_from_another_event_should_return_false(mocker, organizer2, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = False
    assert not filters.is_installer(organizer2.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer2.event_user.user, event1.event_slug)


# is_collaborator
@pytest.mark.django_db
def test_is_collaborator_with_not_eventuser_should_return_false(user1, event1):
    assert not filters.is_collaborator(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_eventuser_not_collaborator_should_return_false(event_user1, event1):
    assert not filters.is_collaborator(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_collaborator_from_another_event_should_return_false(collaborator2, event1):
    assert not filters.is_collaborator(collaborator2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_collaborator_should_return_true(collaborator1, event1):
    assert filters.is_collaborator(collaborator1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_organizer_should_return_true(mocker, organizer1, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = True
    assert filters.is_collaborator(organizer1.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_organizer_from_another_event_should_return_false(mocker, organizer2, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = False
    assert not filters.is_collaborator(organizer2.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer2.event_user.user, event1.event_slug)


# is_reviewer
@pytest.mark.django_db
def test_is_reviewer_with_not_eventuser_should_return_false(user1, event1):
    assert not filters.is_reviewer(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_eventuser_not_reviewer_should_return_false(event_user1, event1):
    assert not filters.is_reviewer(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_reviewer_from_another_event_should_return_false(reviewer2, event1):
    assert not filters.is_reviewer(reviewer2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_reviewer_should_return_true(reviewer1, event1):
    assert filters.is_reviewer(reviewer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_organizer_should_return_true(mocker, organizer1, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = True
    assert filters.is_reviewer(organizer1.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_organizer_from_another_event_should_return_false(mocker, organizer2, event1):
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = False
    assert not filters.is_reviewer(organizer2.event_user.user, event1.event_slug)
    mock_is_organizer.assert_called_once_with(organizer2.event_user.user, event1.event_slug)


# is_organizer
@pytest.mark.django_db
def test_is_organizer_with_anonymous_user_should_return_false(event1):
    assert not filters.is_organizer(AnonymousUser(), event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_user_not_eventuser_should_return_false(user1, event1):
    assert not filters.is_organizer(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_eventuser_not_organizer_should_return_false(event_user1, event1):
    assert not filters.is_organizer(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_organizer_from_another_event_should_return_false(organizer2, event1):
    assert not filters.is_organizer(organizer2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_organizer_should_return_true(organizer1, event1):
    assert filters.is_organizer(organizer1.event_user.user, event1.event_slug)


# is_attendee
@pytest.mark.django_db
def test_is_attendee_with_user_not_is_attendee_should_return_false(user1, event1):
    assert not filters.is_attendee(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_attendee_with_attendee_from_another_event_should_return_false(attendee_from_event_user2, event1):
    assert not filters.is_attendee(attendee_from_event_user2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_attendee_with_attendee_should_return_false(attendee_from_event_user1, event1):
    assert filters.is_attendee(attendee_from_event_user1.event_user.user, event1.event_slug)


# can_take_attendance
@pytest.mark.django_db
def test_can_take_attendance_with_user_without_perm_should_return_false(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=False)
    assert not filters.can_take_attendance(user1, event1.event_slug)


@pytest.mark.django_db
def test_can_take_attendance_with_user_with_perms_should_return_true(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=True)
    assert filters.can_take_attendance(user1, event1.event_slug)


@pytest.mark.django_db
def test_can_take_attendance_should_call_user_has_perm_with_add_attendee(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=True)
    filters.can_take_attendance(user1, event1.event_slug)
    user1.has_perm.assert_any_call('manager.add_attendee')


@pytest.mark.django_db
def test_can_take_attendance_should_call_user_has_perm_with_can_take_attendance(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=True)
    filters.can_take_attendance(user1, event1.event_slug)
    user1.has_perm.assert_any_call('manager.can_take_attendance')


# add
@pytest.mark.parametrize('num1, num2, expected', [
    (0, 0, 0),
    (0, 1, 1),
    (2, 0, 2),
    (5, 7, 12)
])
def test_add_should_return_sum(num1, num2, expected):
    assert filters.add(num1, num2) == expected


# installer_level
@pytest.mark.parametrize('value, expected', [
    ('0', _('N/A')),
    ('1', _('Beginner')),
    ('2', _('Medium')),
    ('3', _('Advanced')),
    ('4', _('Super Hacker')),
])
def test_installer_level_should_return_correct_text(value, expected):
    assert filters.installer_level(value) == expected


# sorted_days
@pytest.mark.django_db
def test_sorted_days_with_empty_list_should_return_empty_list():
    assert filters.sorted_days([]) == []


@pytest.mark.django_db
def test_sorted_days_with_one_day_should_return_this_day(event_date_24_01_2019):
    assert filters.sorted_days([event_date_24_01_2019]) == [24]


@pytest.mark.django_db
def test_sorted_days_with_two_days_should_return_sorted_days(event_date_24_01_2019, event_date_25_01_2019):
    days = [event_date_24_01_2019, event_date_25_01_2019]
    assert filters.sorted_days(days) == [24, 25]


@pytest.mark.django_db
def test_sorted_days_with_four_days_should_return_sorted_days(
        event_date_24_01_2019, event_date_25_01_2019,
        event_date_26_01_2019, event_date_27_01_2019
):
    days = [
        event_date_27_01_2019, event_date_26_01_2019,
        event_date_24_01_2019, event_date_25_01_2019
    ]
    assert filters.sorted_days(days) == [24, 25, 26, 27]


# keyvalue
@pytest.mark.parametrize('dictionary, key, expected', [
    ({'key': 1}, 'key', 1),
    ({'key2': 2}, 'key2', 2),
    ({'key2': 2, 'key': 1}, 'key2', 2)
])
def test_keyvalue_should_return_correct_value(dictionary, key, expected):
    assert filters.keyvalue(dictionary, key) == expected


# exists_vote
@pytest.mark.django_db
def test_exists_vote_when_user_without_votes_should_return_false(user1, activity1):
    assert not filters.exists_vote(user1, activity1)


@pytest.mark.django_db
def test_exists_vote_when_user_vote_only_another_activity_should_return_false(user1, activity1, activity2):
    autofixture.create_one('vote.Vote', {'user_id': user1.id, 'object_id': activity2.id})
    assert not filters.exists_vote(user1, activity1)


@pytest.mark.django_db
def test_exists_vote_when_exists_vote_should_return_true(user1, activity1):
    autofixture.create_one('vote.Vote', {'user_id': user1.id, 'object_id': activity1.id})
    assert filters.exists_vote(user1, activity1)


# is_speaker
@pytest.mark.django_db
def test_is_speaker_when_user_not_owner_should_return_false(event_user1, event1):
    assert not filters.is_speaker(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_speaker_when_user_is_activity_owner_in_another_event_should_return_false(event_user1, event1, activity2):
    activity2.owner = event_user1
    activity2.save()
    assert not filters.is_speaker(event_user1.user, event1.event_slug)


@pytest.mark.django_db
def test_is_speaker_when_user_is_activity_owner_in_event_should_return_true(event_user1, event1, activity1):
    activity1.owner = event_user1
    activity1.save()
    assert filters.is_speaker(event_user1.user, event1.event_slug)


# can_register_as_collaborator
@pytest.mark.django_db
def test_can_register_as_collaborator_with_event_without_collaborators_should_return_false(event1):
    event1.use_collaborators = False
    event1.save()
    anonymous_user = AnonymousUser()
    assert not filters.can_register_as_collaborator(anonymous_user, event1)


@pytest.mark.django_db
def test_can_register_as_collaborator_with_authenticated_collaborator_and_event_with_collaborators_should_return_false(event1, mocker):
    mock_is_collaborator = mocker.patch('manager.templatetags.filters.is_collaborator')
    mock_is_collaborator.return_value = True
    event1.use_collaborators = True
    event1.save()
    user = mocker.MagicMock()
    user.is_authenticated = True
    assert not filters.can_register_as_collaborator(user, event1)
    mock_is_collaborator.assert_called_once_with(user, event1.event_slug)


@pytest.mark.django_db
def test_can_register_as_collaborator_with_anonymous_user_and_event_with_collaborators_should_return_true(event1):
    event1.use_collaborators = True
    event1.save()
    anonymous_user = AnonymousUser()
    assert filters.can_register_as_collaborator(anonymous_user, event1)


@pytest.mark.django_db
def test_can_register_as_collaborator_with_user_not_collaborator_and_event_with_collaborators_should_return_true(event1, user1, mocker):
    mock_is_collaborator = mocker.patch('manager.templatetags.filters.is_collaborator')
    mock_is_collaborator.return_value = False
    event1.use_collaborators = True
    event1.save()
    assert filters.can_register_as_collaborator(user1, event1)
    mock_is_collaborator.assert_called_once_with(user1, event1.event_slug)


# can_register_as_installer
@pytest.mark.django_db
def test_can_register_as_installer_with_event_without_installers_should_return_false(event1):
    event1.use_installers = False
    event1.save()
    anonymous_user = AnonymousUser()
    assert not filters.can_register_as_installer(anonymous_user, event1)


@pytest.mark.django_db
def test_can_register_as_installer_with_authenticated_installer_and_event_with_installers_should_return_false(event1, mocker):
    mock_is_installer = mocker.patch('manager.templatetags.filters.is_installer')
    mock_is_installer.return_value = True
    event1.use_installers = True
    event1.save()
    user = mocker.MagicMock()
    user.is_authenticated = True
    assert not filters.can_register_as_installer(user, event1)
    mock_is_installer.assert_called_once_with(user, event1.event_slug)


@pytest.mark.django_db
def test_can_register_as_installer_with_anonymous_user_and_event_with_installers_should_return_true(event1):
    event1.use_installers = True
    event1.save()
    anonymous_user = AnonymousUser()
    assert filters.can_register_as_installer(anonymous_user, event1)


@pytest.mark.django_db
def test_can_register_as_installer_with_user_not_installer_and_event_with_installers_should_return_true(event1, user1, mocker):
    mock_is_installer = mocker.patch('manager.templatetags.filters.is_installer')
    mock_is_installer.return_value = False
    event1.use_installers = True
    event1.save()
    assert filters.can_register_as_installer(user1, event1)
    mock_is_installer.assert_called_once_with(user1, event1.event_slug)


# can_register_installations
@pytest.mark.django_db
def test_can_register_installations_with_anonymous_user_should_return_false(event1):
    anonymous_user = AnonymousUser()
    assert not filters.can_register_installations(anonymous_user, event1)


@pytest.mark.django_db
def test_can_register_installations_with_authenticated_user_and_event_without_installations_should_return_false(event1, mocker):
    event1.use_installations = False
    event1.save()
    user = mocker.MagicMock()
    user.is_authenticated = True
    assert not filters.can_register_installations(user, event1)


@pytest.mark.django_db
def test_can_register_installations_with_authenticated_user_not_intaller_and_event_with_installations_should_return_false(event1, mocker):
    mock_is_installer = mocker.patch('manager.templatetags.filters.is_installer')
    mock_is_installer.return_value = False
    event1.use_installations = True
    event1.save()
    user = mocker.MagicMock()
    user.is_authenticated = True
    assert not filters.can_register_installations(user, event1)
    mock_is_installer.assert_called_once_with(user, event1.event_slug)


@pytest.mark.django_db
def test_can_register_installations_with_authenticated_intaller_and_event_with_installations_should_return_true(event1, mocker):
    mock_is_installer = mocker.patch('manager.templatetags.filters.is_installer')
    mock_is_installer.return_value = True
    event1.use_installations = True
    event1.save()
    user = mocker.MagicMock()
    user.is_authenticated = True
    assert filters.can_register_installations(user, event1)
    mock_is_installer.assert_called_once_with(user, event1.event_slug)


# show_collaborators_tab
@pytest.mark.django_db
def test_show_collaborators_tab_when_can_register_as_collaborator_should_return_true(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = True
    assert filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)


@pytest.mark.django_db
def test_show_collaborators_tab_when_can_register_as_installer_should_return_true(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = False
    mock_can_register_as_installer = mocker.patch('manager.templatetags.filters.can_register_as_installer')
    mock_can_register_as_installer.return_value = True
    assert filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)
    mock_can_register_as_installer.assert_called_once_with(user1, event1)


@pytest.mark.django_db
def test_show_collaborators_tab_when_can_register_installations_should_return_true(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = False
    mock_can_register_as_installer = mocker.patch('manager.templatetags.filters.can_register_as_installer')
    mock_can_register_as_installer.return_value = False
    mock_can_register_installations = mocker.patch('manager.templatetags.filters.can_register_installations')
    mock_can_register_installations.return_value = True
    assert filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)
    mock_can_register_as_installer.assert_called_once_with(user1, event1)
    mock_can_register_installations.assert_called_once_with(user1, event1)


@pytest.mark.django_db
def test_show_collaborators_tab_when_can_take_attendance_should_return_true(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = False
    mock_can_register_as_installer = mocker.patch('manager.templatetags.filters.can_register_as_installer')
    mock_can_register_as_installer.return_value = False
    mock_can_register_installations = mocker.patch('manager.templatetags.filters.can_register_installations')
    mock_can_register_installations.return_value = False
    mock_can_take_attendance = mocker.patch('manager.templatetags.filters.can_take_attendance')
    mock_can_take_attendance.return_value = True
    assert filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)
    mock_can_register_as_installer.assert_called_once_with(user1, event1)
    mock_can_register_installations.assert_called_once_with(user1, event1)
    mock_can_take_attendance.assert_called_once_with(user1, event1.event_slug)


@pytest.mark.django_db
def test_show_collaborators_tab_when_is_organizer_should_return_true(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = False
    mock_can_register_as_installer = mocker.patch('manager.templatetags.filters.can_register_as_installer')
    mock_can_register_as_installer.return_value = False
    mock_can_register_installations = mocker.patch('manager.templatetags.filters.can_register_installations')
    mock_can_register_installations.return_value = False
    mock_can_take_attendance = mocker.patch('manager.templatetags.filters.can_take_attendance')
    mock_can_take_attendance.return_value = False
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = True
    assert filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)
    mock_can_register_as_installer.assert_called_once_with(user1, event1)
    mock_can_register_installations.assert_called_once_with(user1, event1)
    mock_can_take_attendance.assert_called_once_with(user1, event1.event_slug)
    mock_is_organizer.assert_called_once_with(user1, event1.event_slug)


@pytest.mark.django_db
def test_show_collaborators_tab_when_all_checks_are_false_should_return_false(user1, event1, mocker):
    mock_can_register_as_collaborator = mocker.patch('manager.templatetags.filters.can_register_as_collaborator')
    mock_can_register_as_collaborator.return_value = False
    mock_can_register_as_installer = mocker.patch('manager.templatetags.filters.can_register_as_installer')
    mock_can_register_as_installer.return_value = False
    mock_can_register_installations = mocker.patch('manager.templatetags.filters.can_register_installations')
    mock_can_register_installations.return_value = False
    mock_can_take_attendance = mocker.patch('manager.templatetags.filters.can_take_attendance')
    mock_can_take_attendance.return_value = False
    mock_is_organizer = mocker.patch('manager.templatetags.filters.is_organizer')
    mock_is_organizer.return_value = False
    assert not filters.show_collaborators_tab(user1, event1)
    mock_can_register_as_collaborator.assert_called_once_with(user1, event1)
    mock_can_register_as_installer.assert_called_once_with(user1, event1)
    mock_can_register_installations.assert_called_once_with(user1, event1)
    mock_can_take_attendance.assert_called_once_with(user1, event1.event_slug)
    mock_is_organizer.assert_called_once_with(user1, event1.event_slug)
