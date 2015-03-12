from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from manager.models import Installation


def create_installers_group():
    content_type = ContentType.objects.get_for_model(Installation)
    create_installation = Permission.objects.get(codename='add_installation',
                                                 name='Can add installation',
                                                 content_type=content_type)
    installers = Group.objects.create(name='Installers')
    installers.permissions.add(create_installation)
    installers.save()
    return installers


def add_installer_perms(user):
    group = None
    try:
        group = Group.objects.get(name='Installers')
    except Group.DoesNotExist:
        group = create_installers_group()
    user.groups.add(group)
    user.save()
    return user
