from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import Q

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


def add_installer_perms(user):
    group, created = Group.objects.get_or_create(name='Installers')
    if created:
        group = create_installers_group()
    user.groups.add(group)
    user.save()
    return user


def add_collaborator_perms(user):
    group, created = Group.objects.get_or_create(name='Collaborators')
    if created:
        group = create_collaborators_group()
    user.groups.add(group)
    user.save()
    return user


def is_installer(user):
    if Installer.objects.filter(collaborator__user=user).exists():
        return True
    raise PermissionDenied
