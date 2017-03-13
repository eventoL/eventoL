from django import template, forms
from django.utils.translation import ugettext_lazy as _

from manager.models import Installer, Collaborator, Organizer, EventUser

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='is_checkbox')
def is_checkbox(boundfield):
    """Return True if this field's widget is a CheckboxInput."""
    return isinstance(boundfield.field.widget, forms.CheckboxInput) or \
           isinstance(boundfield.field.widget, forms.CheckboxSelectMultiple)


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
    """Search if the user is registered for the event in any way"""
    return EventUser.objects.filter(user=user, event__slug__iexact=event_slug).exists()


@register.filter(name='is_installer')
def is_installer(user, event_slug):
    return Installer.objects.filter(event_user__user=user, event_user__event__slug__iexact=event_slug).exists() or \
           is_organizer(user, event_slug)


@register.filter(name='is_collaborator')
def is_collaborator(user, event_slug):
    return Collaborator.objects.filter(event_user__user=user, event_user__event__slug__iexact=event_slug).exists() or \
           is_organizer(user, event_slug)


@register.filter(name='is_organizer')
def is_organizer(user, event_slug):
    return Organizer.objects.filter(event_user__user=user, event_user__event__slug__iexact=event_slug).exists()


@register.filter(name='can_take_attendance')
def can_take_attendance(user, event_slug):
    return user.has_perm('manager.add_attendee') or user.has_perm('manager.can_take_attendance')


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
    else:
        return _('N/A')
