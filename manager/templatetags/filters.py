from django import template, forms
from manager.models import Installer, Collaborator

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


@register.filter(name='is_odd')
def is_odd(number):
    """Return True if the number is odd"""
    return number & 1


@register.filter(name='is_installer')
def is_installer(user):
    return Installer.objects.filter(collaborator__user=user).exists()


@register.filter(name='is_sede_staff')
def is_sede_staff(sede_url, user):
    if user.is_superuser:
        return True
    try:
        exists_collaborator = Collaborator.objects.filter(user=user, sede__url=sede_url).exists()
        return exists_collaborator and user.is_staff
    except Exception:
        return False


@register.filter(name='bootstrap_cols')
def bootstrap_cols(elements):
    cant = len(elements)
    return int(round(12/cant)) if cant < 5 else 3
