import json

from django import forms, template
from django.utils.translation import ugettext_lazy as _
from vote.models import Vote

from manager.constants import (
    ADD_ATTENDEE_PERMISSION_CODE_NAME, CAN_TAKE_ATTENDANCE_PERMISSION_CODE_NAME
)
from manager.models import (
    Activity, Attendee, Collaborator, EventUser, Installer, Organizer, Reviewer
)

register = template.Library()


@register.filter(name='get_contact_url')
def get_contact_url(contact):
    """
    Returns contact url
    """
    if contact.type.validate == '2':
        return 'mailto:{}'.format(contact.url)
    return contact.url


@register.filter(name='get_schedule_size')
def get_schedule_size(rooms):
    """
        Returns a schedule min width
    """
    return len(json.loads(rooms)) * 200


@register.filter(name='get_schedule_date')
def get_schedule_date(dic, key):
    """
    Returns an item from a dictionary
    """
    return json.loads(dic.get(key)).get('datestring')


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='is_checkbox')
def is_checkbox(boundfield):
    """Return True if this field's widget is a CheckboxInput."""
    widget = boundfield.field.widget
    is_checkbox_input = isinstance(widget, forms.CheckboxInput)
    is_checkbox_select = isinstance(widget, forms.CheckboxSelectMultiple)
    return is_checkbox_input or is_checkbox_select


@register.filter(name='is_datetime')
def is_datetime(boundfield):
    """Return True if this field's widget is a DateInput."""
    return isinstance(boundfield.field.widget, forms.DateTimeInput)


@register.filter(name='is_fileinput')
def is_fileinput(boundfield):
    """Return True if this field's widget is a FileField."""
    return isinstance(boundfield.field.widget, forms.FileInput)


@register.filter(name='is_select')
def is_select(boundfield):
    """Return True if this field's widget is a Select Combo."""
    return isinstance(boundfield.field.widget, forms.Select)


@register.filter(name='is_odd')
def is_odd(number):
    """Return True if the number is odd"""
    return bool(number & 1)


@register.filter(name='is_registered')
def is_registered(user, event_slug):
    """Search if the user is registered for the event"""
    return EventUser.objects.filter(
        user=user, event__event_slug=event_slug).exists()


@register.filter(name='is_registered_any_way')
def is_registered_any_way(user, event_slug):
    """Search if the user is registered for the event in any way"""
    return is_attendee(user, event_slug) or is_registered(user, event_slug)


@register.filter(name='is_installer')
def is_installer(user, event_slug):
    exists_installer = Installer.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_installer or is_organizer(user, event_slug)


@register.filter(name='is_collaborator')
def is_collaborator(user, event_slug):
    exists_collaborator = Collaborator.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_collaborator or is_organizer(user, event_slug)


@register.filter(name='is_reviewer')
def is_reviewer(user, event_slug):
    exists_reviewer = Reviewer.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_reviewer or is_organizer(user, event_slug)


@register.filter(name='is_organizer')
def is_organizer(user, event_slug):
    return user.is_authenticated and Organizer.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()


@register.filter(name='is_attendee')
def is_attendee(user, event_slug):
    exists_attendee = Attendee.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_attendee


@register.filter(name=CAN_TAKE_ATTENDANCE_PERMISSION_CODE_NAME)
def can_take_attendance(user, _):
    has_add = user.has_perm(f'manager.{ADD_ATTENDEE_PERMISSION_CODE_NAME}')
    has_take = user.has_perm(f'manager.{CAN_TAKE_ATTENDANCE_PERMISSION_CODE_NAME}')
    return has_add or has_take


@register.filter(name='add')
def add(base, value_to_sum):
    return base + value_to_sum


INSTALLER_LEVELS = {
    '1': _('Beginner'),
    '2': _('Medium'),
    '3': _('Advanced'),
    '4': _('Super Hacker')
}

@register.filter(name='installer_level')
def installer_level(value):
    if value in INSTALLER_LEVELS:
        return INSTALLER_LEVELS[value]
    return _('N/A')


@register.filter(name='sorted_days')
def sorted_days(dates):
    return sorted([date.date.day for date in dates])


@register.filter(name='keyvalue')
def keyvalue(data, key):
    return data[key]


@register.filter(name='exists_vote')
def exists_vote(user, activity):
    return Vote.objects.filter(user_id=user.id, object_id=activity.id).exists()


@register.filter(name='is_speaker')
def is_speaker(user, event_slug):
    return Activity.objects.filter(owner__user=user, event__event_slug=event_slug).exists()


def can_register_as_collaborator(user, event):
    if event.use_collaborators:
        if not user.is_authenticated or not is_collaborator(user, event.event_slug):
            return True
    return False


def can_register_as_installer(user, event):
    if event.use_installers:
        if not user.is_authenticated or not is_installer(user, event.event_slug):
            return True
    return False


def can_register_installations(user, event):
    if user.is_authenticated:
        if event.use_installations and is_installer(user, event.event_slug):
            return True
    return False


@register.filter(name='show_collaborators_tab')
def show_collaborators_tab(user, event):
    return (
        can_register_as_collaborator(user, event) or
        can_register_as_installer(user, event) or
        can_register_installations(user, event) or
        can_take_attendance(user, event.event_slug) or
        is_organizer(user, event.event_slug)
    )
