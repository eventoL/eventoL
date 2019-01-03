import json

from django import forms, template
from django.utils.translation import ugettext_lazy as _

from manager.models import (
    Activity,
    Attendee,
    Collaborator,
    EventUser,
    Installer,
    Organizer,
    Reviewer
)
from vote.models import Vote

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
    return field.as_widget(attrs={"class": css})


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
    exists_collaborator = Reviewer.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_collaborator or is_organizer(user, event_slug)


@register.filter(name='is_organizer')
def is_organizer(user, event_slug):
    return Organizer.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()


@register.filter(name='is_attendee')
def is_attendee(user, event_slug):
    exists_attendee = Attendee.objects.filter(
        event_user__user=user,
        event_user__event__event_slug=event_slug).exists()
    return exists_attendee


@register.filter(name='can_take_attendance')
def can_take_attendance(user, _):
    has_add = user.has_perm('manager.add_attendee')
    has_take = user.has_perm('manager.can_take_attendance')
    return has_add or has_take


@register.filter(name='add')
def add(base, value_to_sum):
    return base + value_to_sum


@register.filter(name='installer_level')
def installer_level(value):
    if value == '1':
        return _('Beginner')
    elif value == '2':
        return _('Medium')
    elif value == '3':
        return _('Advanced')
    elif value == '4':
        return _('Super Hacker')
    return _('N/A')


@register.filter(name='as_days')
def as_days(dates):
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
