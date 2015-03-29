from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from manager.models import Installation, Installer


def create_installers_group():
    content_type = ContentType.objects.get_for_model(Installation)
    create_installation = Permission.objects.get(codename='add_installation',
                                                 name='Can add Installation',
                                                 content_type=content_type)
    installers = Group.objects.create(name='Installers')
    installers.permissions.add(create_installation)
    installers.save()
    return installers


def add_installer_perms(user):
    group = Group.objects.get_or_create(name='Installers')[0]
    user.groups.add(group)
    user.save()
    return user


def is_installer(user):
    if Installer.objects.filter(collaborator__user=user).exists():
        return True
    if user.is_staff:
        return True
    raise PermissionDenied
