from django.contrib.auth.models import Permission, Group
from django.utils.decorators import available_attrs
from functools import wraps
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from manager.models import Installer, Organizer, EventUser, NonRegisteredAttendee, Collaborator


def is_installer(user, event_slug=None, *args, **kwargs):
    return event_slug and (
        Installer.objects.filter(eventUser__user=user, eventUser__event__slug__iexact=event_slug).exists() or \
        is_organizer(user, event_slug=event_slug))


def add_attendance_permission(user):
    content_type = ContentType.objects.get_for_model(NonRegisteredAttendee)
    user.user_permissions.add(Permission.objects.get(content_type=content_type, codename='add_nonregisteredattendee'))
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='change_nonregisteredattendee'))

    content_type = ContentType.objects.get_for_model(EventUser)
    attendance_permission = None

    if Permission.objects.filter(codename='can_take_attendance', name='Can Take Attendance',
                                 content_type=content_type).exists():
        attendance_permission = Permission.objects.get(codename='can_take_attendance', name='Can Take Attendance',
                                                       content_type=content_type)
    else:
        attendance_permission = Permission.objects.create(codename='can_take_attendance', name='Can Take Attendance',
                                                          content_type=content_type)

    user.user_permissions.add(attendance_permission)

    user.user_permissions.add(Permission.objects.get(content_type=content_type, codename='change_eventuser'))


def create_organizers_group():
    organizers = None
    if not Group.objects.filter(name='Organizers').exists():
        perms = ['add_contactmessage', 'change_contactmessage', 'delete_contactmessage', 'add_nonregisteredattendee',
                 'change_nonregisteredattendee', 'delete_nonregisteredattendee', 'add_eventuser', 'change_eventuser',
                 'delete_eventuser', 'add_collaborator', 'change_collaborator', 'delete_collaborator', 'add_organizer',
                 'change_organizer', 'delete_organizer', 'add_attendee', 'change_attendee', 'delete_attendee',
                 'add_installationattendee', 'change_installationattendee', 'delete_installationattendee',
                 'add_installer',
                 'change_installer', 'delete_installer', 'add_speaker', 'change_speaker', 'delete_speaker', 'add_room',
                 'change_room', 'delete_room', 'add_activity', 'change_activity', 'delete_activity', 'add_talkproposal',
                 'change_talkproposal', 'delete_talkproposal', 'add_installation', 'change_installation',
                 'delete_installation']
        organizers = Group.objects.create(name='Organizers')
        for perm in perms:
            organizers.permissions.add(Permission.objects.get(codename=perm))

        organizers.save()
    else:
        organizers = Group.objects.get(name='Organizers')

    return organizers


def add_organizer_permissions(user):
    organizers = create_organizers_group()
    user.groups.add(organizers)
    user.is_staff = True
    user.save()


def is_organizer(user, event_slug=None, *args, **kwargs):
    return event_slug and Organizer.objects.filter(eventUser__user=user,
                                                   eventUser__event__slug__iexact=event_slug).exists()


def is_collaborator(user, event_slug=None, *args, **kwargs):
    return event_slug and (
        Collaborator.objects.filter(eventUser__user=user, eventUser__event__slug__iexact=event_slug).exists() or \
        is_collaborator(user, event_slug=event_slug))


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
            return HttpResponseRedirect(reverse(name_redirect, args=[kwargs['event_slug']]))

        return _wrapped_view

    return decorator
