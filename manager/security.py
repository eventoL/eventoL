from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.utils.decorators import available_attrs
from functools import wraps
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from manager.models import Installer, Organizer, Collaborator


def create_collaborators_group():
    collaborators = Group.objects.get(name='Collaborators')
    perms = Permission.objects.filter(
        Q(content_type__app_label='manager') |
        Q(content_type__app_label='admin') |
        Q(content_type__app_label='sessions')
    )
    for perm in perms:
        collaborators.permissions.add(perm)
    collaborators.save()
    return collaborators


def add_collaborator_perms(user):
    group, created = Group.objects.get_or_create(name='Collaborators')
    if created:
        group = create_collaborators_group()
    user.groups.add(group)
    user.is_staff = True
    user.save()
    return user


def is_installer(user, event_slug=None):
    return event_slug and Installer.objects.filter(eventUser__user=user, eventUser__event__slug=event_slug).exists()


def is_organizer(user, event_slug=None):
    return event_slug and Organizer.objects.filter(eventUser__user=user, eventUser__event__slug=event_slug).exists()


def is_collaborator(user, event_slug=None):
    return event_slug and Collaborator.objects.filter(eventUser__user=user, eventUser__event__slug=event_slug).exists()


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