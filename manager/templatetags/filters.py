from django import template, forms
from manager.models import Installer, Collaborator, Organizer, EventUser, Attendee, InstallationAttendee
from django.utils.translation import ugettext_lazy as _

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


@register.filter(name='can_register')
def can_register(user, event_slug):
    """Search if the user is registered for the event as an attendee"""
    eventuser = EventUser.objects.filter(user=user, event__slug__iexact=event_slug).first()
    if eventuser:
        is_attendee = Attendee.objects.filter(eventUser=eventuser).exists()
        is_installation_attendee = InstallationAttendee.objects.filter(eventUser=eventuser).exists()
        return not(is_attendee or is_installation_attendee)
    return True


@register.filter(name='is_registered')
def is_registered(user, event_slug):
    """Search if the user is registered for the event in any way"""
    return EventUser.objects.filter(user=user, event__slug__iexact=event_slug).exists()


@register.filter(name='is_installer')
def is_installer(user, event_slug):
    return Installer.objects.filter(eventUser__user=user, eventUser__event__slug__iexact=event_slug).exists() or \
        is_organizer(user, event_slug)


@register.filter(name='is_collaborator')
def is_collaborator(user, event_slug):
    return Collaborator.objects.filter(eventUser__user=user, eventUser__event__slug__iexact=event_slug).exists() or \
        is_organizer(user, event_slug)


@register.filter(name='is_organizer')
def is_organizer(user, event_slug):
    return Organizer.objects.filter(eventUser__user=user, eventUser__event__slug__iexact=event_slug).exists()


@register.filter(name='can_take_attendance')
def can_take_attendance(user, event_slug):
    return is_collaborator(user, event_slug) or user.has_perm('manager.add_attendee') or user.has_perm('manager.can_take_attendance')


@register.filter(name='schedule_cols_total')
def schedule_cols_total(elements):
    elems = len(elements)
    if elems <= 3:
        return 12
    elif elems <= 5:
        return len(elements) * 3 + 1
    return len(elements) * 2 + 1


@register.filter(name='schedule_cols_first')
def schedule_cols_first(elements):
    elems = len(elements)
    if elems <= 2:
        return 2
    elif elems == 3:
        return 3
    return 1


@register.filter(name='schedule_cols_other')
def schedule_cols_other(elements):
    elems = len(elements)
    if elems == 1:
        return 10
    elif elems == 2:
        return 5
    elif elems <= 5:
        return 3
    return 2

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
