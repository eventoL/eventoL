# pylint: disable=invalid-name,line-too-long,too-many-public-methods,
import pytest

from django import forms
from manager.templatetags import filters


# get_contact_url
# get_schedule_size
# get_schedule_date
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
def test_is_installer_with_organizer_should_return_true(organizer1, event1):
    assert filters.is_installer(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_installer_with_organizer_from_another_event_should_return_false(organizer2, event1):
    assert not filters.is_installer(organizer2.event_user.user, event1.event_slug)

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
def test_is_collaborator_with_organizer_should_return_true(organizer1, event1):
    assert filters.is_collaborator(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_collaborator_with_organizer_from_another_event_should_return_false(organizer2, event1):
    assert not filters.is_collaborator(organizer2.event_user.user, event1.event_slug)


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
def test_is_reviewer_with_organizer_should_return_true(organizer1, event1):
    assert filters.is_reviewer(organizer1.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_reviewer_with_organizer_from_another_event_should_return_false(organizer2, event1):
    assert not filters.is_reviewer(organizer2.event_user.user, event1.event_slug)


# is_organizer
@pytest.mark.django_db
def test_is_organizer_with_eventuser_not_organizer_should_return_false(user1, event1):
    assert not filters.is_organizer(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_user_not_eventuser_should_return_false(user1, event1):
    assert not filters.is_organizer(user1, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_organizer_from_another_event_should_return_false(organizer2, event1):
    assert not filters.is_organizer(organizer2.event_user.user, event1.event_slug)


@pytest.mark.django_db
def test_is_organizer_with_organizer_should_return_true(organizer1, event1):
    assert filters.is_organizer(organizer1.event_user.user, event1.event_slug)


# is_attendee


# can_take_attendance
@pytest.mark.django_db
def test_can_take_attendance_with_user_without_perm_should_return_false(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=False)
    assert not filters.can_take_attendance(user1, event1.event_slug)


@pytest.mark.django_db
def test_if_is_collaborator_and_has_perm_can_take_attendance_return_true(mocker, user1, event1):
    user1.has_perm = mocker.Mock(return_value=True)
    assert filters.can_take_attendance(user1, event1.event_slug)


# add
# installer_level
# as_days
# keyvalue
# exists_vote
# is_speaker
# show_collaborators_tab
