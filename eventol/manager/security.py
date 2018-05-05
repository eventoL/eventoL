from functools import wraps

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs

from manager.models import Attendee, Collaborator, Installer, Organizer


def is_installer(user, event_uid=None, **__):
    return event_uid and (
        Installer.objects.filter(
            event_user__user=user,
            event_user__event__uid=event_uid).exists() or
        is_organizer(user, event_uid=event_uid))


def get_or_create_attendance_permission():
    attendance_permission = None
    content_type = ContentType.objects.get_for_model(Attendee)
    if Permission.objects.filter(codename='can_take_attendance',
                                 content_type=content_type).exists():
        attendance_permission = Permission.objects.get(
            codename='can_take_attendance',
            content_type=content_type)
    else:
        attendance_permission = Permission.objects.create(
            codename='can_take_attendance', name='Can Take Attendance',
            content_type=content_type)
    return attendance_permission


def add_attendance_permission(user):
    content_type = ContentType.objects.get_for_model(Attendee)
    if Permission.objects.filter(content_type=content_type,
                                 codename='add_attendee').exists():
        add_attendee_permission = Permission.objects.get(
            content_type=content_type, codename='add_attendee')
    else:
        add_attendee_permission = Permission.objects.create(
            content_type=content_type, name='Add Attendee',
            codename='add_attendee')
    if Permission.objects.filter(content_type=content_type,
                                 codename='change_attendee').exists():
        change_attendee_permission = Permission.objects.get(
            content_type=content_type,
            codename='change_attendee')
    else:
        change_attendee_permission = Permission.objects.create(
            content_type=content_type, name='Change Attendee',
            codename='change_attendee')
    user.user_permissions.add(add_attendee_permission)
    user.user_permissions.add(change_attendee_permission)
    attendance_permission = get_or_create_attendance_permission()
    user.user_permissions.add(attendance_permission)


def create_organizers_group():
    organizers = Group.objects.filter(name__iexact='Organizers').first()
    get_or_create_attendance_permission()
    if not organizers:
        perms = ['add_event', 'change_event', 'delete_event',
                 'add_contactmessage', 'change_contactmessage',
                 'delete_contactmessage', 'add_attendee',
                 'can_take_attendance', 'add_contact', 'change_contact',
                 'delete_contact', 'change_attendee', 'delete_attendee',
                 'add_eventuser', 'change_eventuser', 'delete_collaborator',
                 'delete_eventuser', 'add_collaborator', 'change_collaborator',
                 'add_organizer', 'change_organizer', 'delete_organizer',
                 'add_installer', 'change_installer', 'delete_installer',
                 'add_room', 'change_room', 'delete_room', 'add_activity',
                 'change_activity', 'delete_activity', 'delete_installation',
                 'add_installation', 'change_installation',
                 'add_installationmessage', 'change_installationmessage',
                 'delete_installationmessage', 'add_eventdate',
                 'change_eventdate', 'delete_eventdate', 'add_software',
                 'change_software', 'delete_software', 'add_hardware',
                 'change_hardware', 'delete_hardware', 'add_contacttype',
                 'change_contacttype', 'delete_contacttype']
        organizers = Group.objects.create(name='Organizers')
        for perm in perms:
            organizers.permissions.add(Permission.objects.get(codename=perm))
        organizers.save()
    return organizers


def create_reporters_group():
    reporters = Group.objects.filter(name__iexact='Reporters').first()
    if not reporters:
        perms = ['add_contactmessage', 'change_contactmessage',
                 'delete_contactmessage', 'add_attendee', 'change_eventuser',
                 'change_attendee', 'delete_attendee', 'add_eventuser',
                 'delete_eventuser', 'delete_collaborator', 'change_organizer',
                 'add_collaborator', 'change_collaborator', 'add_organizer',
                 'delete_organizer', 'add_installer', 'change_installer',
                 'delete_installer', 'add_room', 'change_room',
                 'delete_room', 'add_activity', 'change_activity',
                 'delete_activity', 'add_installation',
                 'change_installation', 'delete_installation']
        reporters = Group.objects.create(name='Reporters')
        for perm in perms:
            reporters.permissions.add(Permission.objects.get(codename=perm))
        reporters.save()
    return reporters


def add_organizer_permissions(user):
    organizers = create_organizers_group()
    user.groups.add(organizers)
    user.is_staff = True
    user.save()


def is_organizer(user, event_uid=None, **__):
    return event_uid and Organizer.objects.filter(
        event_user__user=user,
        event_user__event__uid=event_uid).exists()


def is_collaborator(user, event_uid=None, **__):
    return event_uid and (
        Collaborator.objects.filter(
            event_user__user=user,
            event_user__event__uid=event_uid).exists() or
        is_organizer(user, event_uid=event_uid))


def is_collaborator_or_installer(user, *args, **kwargs):
    return is_collaborator(user, *args, **kwargs) or is_installer(user, *args, **kwargs)


def user_passes_test(test_func, name_redirect):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(
                reverse(
                    name_redirect,
                    kwargs=kwargs
                )
            )

        return _wrapped_view

    return decorator
