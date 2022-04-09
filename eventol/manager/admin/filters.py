# pylint: disable=no-self-use

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from manager.admin.utils import filter_model_queryset_by_user
from manager.models import Event, Hardware, Room, Software


def get_lookups_tuple(user, source_model, target_model, order_field, id_field):
    queryset = filter_model_queryset_by_user(user, source_model)
    ids = queryset.order_by(order_field).values_list(id_field, flat=True).distinct()
    return [(id, str(target_model.objects.get(id=id))) for id in ids if id is not None]


class OwnerFilter(admin.SimpleListFilter):
    title = _('Owner')
    parameter_name = 'owner_user'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, User, 'owner__user__username', 'owner__user'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(owner__user__id=value)


class UserFromEventUserFilter(admin.SimpleListFilter):
    title = _('User')
    parameter_name = 'user_form_event_user'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, User, 'event_user__user__username', 'event_user__user'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(event_user__user__id=value)


class UserFromEventUserSetFilter(UserFromEventUserFilter):
    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, User, 'eventuser__user__username', 'eventuser__user'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(eventuser__user__id=value)


class EventFromEventUserFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event_from_event_user'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Event, 'event_user__event__name', 'event_user__event'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(event_user__event__id=value)


class EventFromEventUserSetFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event_from_event_user'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Event, 'eventuser__event__name', 'eventuser__event'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(eventuser__event__id=value)


class EventFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(request.user, model_admin.model, Event, 'event__name', 'event')

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(event__id=value)


class RoomFilter(admin.SimpleListFilter):
    title = _('Room')
    parameter_name = 'room'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(request.user, model_admin.model, Room, 'room__name', 'room')

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(room__id=value)


class HardwareFilter(admin.SimpleListFilter):
    title = _('Hardware')
    parameter_name = 'hardware'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Hardware, 'hardware__model', 'hardware'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(hardware__id=value)


class SoftwareFilter(admin.SimpleListFilter):
    title = _('Software')
    parameter_name = 'software'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Software, 'software__name', 'software'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(software__id=value)


class InstallerFilter(admin.SimpleListFilter):
    title = _('Installer')
    parameter_name = 'installer'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, User, 'installer__user__username', 'installer__user'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(installer__user__id=value)


class AttendeeFilter(admin.SimpleListFilter):
    title = _('Attendee')
    parameter_name = 'attendee'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, User, 'attendee__user__username', 'attendee__user'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(attendee__user__id=value)


class EventFromInstallerFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event_from_installer'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Event, 'installer__event__name', 'installer__event'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(installer__event__id=value)


class EventFromAttendeeFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event_from_attendee'

    def lookups(self, request, model_admin):
        return get_lookups_tuple(
            request.user, model_admin.model, Event, 'attendee__event__name', 'attendee__event'
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None or not value:
            return queryset
        return queryset.filter(attendee__event__id=value)
