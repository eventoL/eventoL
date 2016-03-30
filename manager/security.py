from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from manager.models import Installer, Organizer, EventUser, NonRegisteredAttendee


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


def is_installer(user):
    if Installer.objects.filter(eventUser__user=user).exists():
        return True
    raise PermissionDenied


def is_organizer(user):
    if Organizer.objects.filter(eventUser__user=user).exists():
        return True
    raise PermissionDenied
