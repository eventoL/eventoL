from functools import wraps

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from manager.constants import (
    ADD_ATTENDEE_PERMISSION_CODE_NAME, ADD_ATTENDEE_PERMISSION_NAME,
    CAN_TAKE_ATTENDANCE_PERMISSION_CODE_NAME, CAN_TAKE_ATTENDANCE_PERMISSION_NAME,
    CHANGE_ATTENDEE_PERMISSION_CODE_NAME, CHANGE_ATTENDEE_PERMISSION_NAME,
    ORGANIZER_GROUP_NAME, ORGANIZER_PERMISSION_CODE_NAMES, REPORTER_GROUP_NAME,
    REPORTER_PERMISSION_CODE_NAMES
)
from manager.models import Activity, Attendee, Collaborator, Installer, Organizer, Reviewer


def get_or_create_attendance_permission():
    content_type = ContentType.objects.get_for_model(Attendee)
    attendance_permission, _ = Permission.objects.get_or_create(
        codename=CAN_TAKE_ATTENDANCE_PERMISSION_CODE_NAME, content_type=content_type,
        defaults=dict(name=CAN_TAKE_ATTENDANCE_PERMISSION_NAME)
    )
    return attendance_permission


def add_attendance_permission(user):
    content_type = ContentType.objects.get_for_model(Attendee)

    add_attendee_permission, _ = Permission.objects.get_or_create(
        codename=ADD_ATTENDEE_PERMISSION_CODE_NAME, content_type=content_type,
        defaults=dict(name=ADD_ATTENDEE_PERMISSION_NAME)
    )

    change_attendee_permission, _ = Permission.objects.get_or_create(
        codename=CHANGE_ATTENDEE_PERMISSION_CODE_NAME, content_type=content_type,
        defaults=dict(name=CHANGE_ATTENDEE_PERMISSION_NAME)
    )

    user.user_permissions.add(add_attendee_permission)
    user.user_permissions.add(change_attendee_permission)
    attendance_permission = get_or_create_attendance_permission()
    user.user_permissions.add(attendance_permission)


def create_permission_group(name, code_names):
    group = Group.objects.filter(name__iexact=name).first()
    if group is None:
        group = Group.objects.create(name=name)
        for permission_codename in code_names:
            permissions = Permission.objects.filter(
                codename=permission_codename, content_type__app_label='manager'
            )
            for permission in permissions.iterator():
                group.permissions.add(permission)
        group.save()
    return group


def create_organizers_group():
    get_or_create_attendance_permission()
    return create_permission_group(ORGANIZER_GROUP_NAME, ORGANIZER_PERMISSION_CODE_NAMES)


def create_reporters_group():
    return create_permission_group(REPORTER_GROUP_NAME, REPORTER_PERMISSION_CODE_NAMES)


def add_organizer_permissions(user):
    organizers = create_organizers_group()
    user.groups.add(organizers)
    user.is_staff = True
    user.save()


def is_speaker(user, event_slug=None):
    if event_slug is None:
        return False

    return Activity.objects.filter(owner__user=user, event__event_slug=event_slug).exists()


def user_has_role(user, role, event_slug=None, check_is_organizer=True):
    if event_slug is None:
        return False

    if role.objects.filter(
            event_user__user=user, event_user__event__event_slug=event_slug
    ).exists():
        return True

    if check_is_organizer:
        return user_has_role(user, Organizer, event_slug=event_slug, check_is_organizer=False)

    return False


def is_installer(user, event_slug=None):
    return user_has_role(user, Installer, event_slug=event_slug)


def is_organizer(user, event_slug=None):
    return user_has_role(user, Organizer, event_slug=event_slug, check_is_organizer=False)


def is_collaborator(user, event_slug=None):
    return user_has_role(user, Collaborator, event_slug=event_slug)


def is_reviewer(user, event_slug=None):
    return user_has_role(user, Reviewer, event_slug=event_slug)


def is_collaborator_or_installer(user, event_slug=None):
    return is_collaborator(user, event_slug=event_slug) or is_installer(user, event_slug=event_slug)


def are_activities_public(user, event_slug=None):
    """
    Return True if activities are public.

    If activities are private only will return true for collaborator users
    """
    if not settings.PRIVATE_ACTIVITIES:
        return True

    if user.is_authenticated:
        return is_reviewer(user, event_slug=event_slug)

    raise PermissionDenied(
        "Only organizers and collaborators are authorized to access the activities list."
    )


def is_activity_public():
    """
    Return True if activities are public.

    If activities are private only will return true for collaborator users or activity owner
    """
    def decorator(view_func):
        @wraps(view_func)

        def _wrapped_view(request, *args, **kwargs):
            activity_id = kwargs['activity_id']
            user = request.user
            activity = get_object_or_404(Activity, pk=activity_id)
            event_slug = kwargs['event_slug']

            if any([
                    activity.status == "2",  # Accepted
                    not settings.PRIVATE_ACTIVITIES,
                    activity.owner.user == user,
                    user.is_authenticated and is_reviewer(user, event_slug=event_slug)
            ]):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied(
                "Only organizers and collaborators are authorized "
                "to access the activities list."
            )
        return _wrapped_view

    return decorator


def user_passes_test(test_func, name_redirect):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if 'event_slug' in kwargs.keys():
                event_slug = kwargs['event_slug']
            else:
                event_slug = args[0]
            if test_func(request.user, event_slug=event_slug):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(
                reverse(
                    name_redirect,
                    args=[event_slug]
                )
            )

        return _wrapped_view

    return decorator
