# pylint: disable=no-init
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext as _
from image_cropping import ImageCroppingMixin
from import_export.admin import ExportMixin

from manager.admin.filters import (
    EventFilter, EventFromAttendeeFilter, EventFromEventUserFilter,
    EventFromEventUserSetFilter, EventFromInstallerFilter, HardwareFilter,
    InstallerFilter, OwnerFilter, RoomFilter, SoftwareFilter,
    UserFromEventUserFilter, UserFromEventUserSetFilter
)
from manager.admin.generics import EventoLAdmin, EventoLEventUserAdmin, ThemeAdmin
from manager.admin.inlines import EventDateAdminInline, EventTagInline
from manager.admin.resources import (
    ActivityResource, AttendeeResource, CollaboratorResource, EventUserAttendanceDateResource,
    EventUserResource, InstallationResource, InstallerResource, OrganizerResource,
    ReviewerResource, TicketResource
)


class ActivityAdmin(ImageCroppingMixin, ExportMixin, EventoLAdmin):
    resource_class = ActivityResource
    list_display = (
        'title', 'event', 'get_owner', 'activity_type', 'start_date', 'end_date',
        'is_dummy', 'status', 'level', 'room',
    )
    list_filter = (
        EventFilter, 'activity_type', 'is_dummy', 'status', 'level', RoomFilter,
        'start_date', 'end_date', 'created_at', OwnerFilter,
    )
    search_fields = (
        'abstract', 'additional_info', 'justification', 'labels', 'long_description',
        'speaker_bio', 'speakers_names', 'title',
    )

    def get_owner(self, obj):
        return obj.owner.user
    get_owner.short_description = _('Owner')
    get_owner.admin_order_field = 'owner__user__username'


class ActivityTypeAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('name',)
    search_fields = ('name',)


class AttendeeAdmin(ExportMixin, EventoLAdmin):
    resource_class = AttendeeResource
    list_display = (
        'get_user', 'get_email', 'event', 'is_installing', 'email_confirmed',
        'registration_date', 'ticket',
    )
    list_filter = (EventFilter, 'is_installing', 'email_confirmed', 'registration_date',)
    search_fields = (
        'additional_info', 'customFields', 'email', 'first_name', 'last_name', 'nickname',
    )

    @staticmethod
    def get_user_str(first_name, last_name, username):
        if first_name is None and last_name is None and username is None:
            return _('Anonymous')
        user_str = '{} {} ({})'.format(first_name, last_name, username)
        return user_str.replace('None', '')

    def get_user(self, obj):
        if obj.event_user is not None:
            user = obj.event_user.user
            return self.get_user_str(user.first_name, user.last_name, user.username)
        return self.get_user_str(obj.first_name, obj.last_name, obj.nickname)
    get_user.short_description = _('User')

    def get_email(self, obj):
        if obj.event_user is not None:
            return obj.event_user.user.email
        return obj.email
    get_email.short_description = _('Email')


class AttendeeAttendanceDateAdmin(EventoLAdmin):
    list_display = ('attendee', 'mode', 'date',)
    list_filter = (EventFromAttendeeFilter, 'mode', 'date',)
    search_fields = (
        'attendee__first_name', 'attendee__last_name', 'attendee__nickname',
        'attendee__email', 'attendee__event_user__user__username',
        'attendee__event_user__user__first_name',
        'attendee__event_user__user__last_name',
        'attendee__event_user__user__email',
    )


class CollaboratorAdmin(EventoLEventUserAdmin):
    resource_class = CollaboratorResource
    list_display = (
        'get_user', 'get_event', 'phone', 'assignation', 'time_availability',
    )
    list_filter = (EventFromEventUserFilter,)
    search_fields = (
        'event_user__user__username', 'event_user__user__first_name',
        'event_user__user__last_name', 'event_user__user__email', 'additional_info',
        'address', 'phone', 'assignation',
    )


class ContactAdmin(EventoLAdmin):
    list_display = ('text', 'type', 'event', 'url',)
    list_filter = ('type', EventFilter,)
    search_fields = ('text', 'type__name', 'url',)


class ContactMessageAdmin(EventoLAdmin):
    list_display = ('name', 'email', 'event',)
    list_filter = (EventFilter,)
    search_fields = ('name', 'email', 'message',)


class ContactTypeAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('name', 'icon_class', 'validate',)
    list_filter = ('icon_class', 'validate',)
    search_fields = ('name', 'icon_class', 'validate',)


class EventAdmin(ImageCroppingMixin, EventoLAdmin):
    inlines = [EventDateAdminInline, EventTagInline]
    exclude = ['tags']
    list_display = (
        'name', 'url', 'registration_closed', 'schedule_confirmed',
        'use_installations', 'use_installers', 'use_collaborators',
        'use_proposals', 'use_talks', 'is_flisol', 'use_schedule',
    )
    list_filter = (
        'registration_closed', 'schedule_confirmed', 'use_installations',
        'use_installers', 'use_collaborators', 'use_proposals', 'use_talks',
        'is_flisol', 'use_schedule', 'created_at', 'tags'
    )
    search_fields = (
        'name', 'event_slug', 'external_url', 'email', 'abstract', 'cname',
        'event_information'
    )

    def url(self, obj):
        if obj.external_url is not None and obj.external_url != '':
            return obj.external_url
        return reverse('index', kwargs=dict(event_slug=obj.event_slug))

    def filter_event(self, events, queryset):
        return queryset.filter(pk__in=[event.pk for event in events])


class EventDateAdmin(EventoLAdmin):
    list_display = ('date', 'event',)
    list_filter = (EventFilter, 'date',)
    search_fields = ('event__name',)


class EventolSettingAdmin(ThemeAdmin):
    search_fields = ('message',)


class EventTagAdmin(ThemeAdmin):
    list_display = (
        'name', 'slug', 'has_background', 'has_logo_header', 'has_logo_landing',
    )
    search_fields = ('name', 'message', 'slug',)


class EventUserAdmin(ExportMixin, EventoLAdmin):
    resource_class = EventUserResource
    list_display = ('user', 'event', 'ticket',)
    list_filter = (EventFilter,)
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name', 'user__email', 'event__name',
    )


class EventUserAttendanceDateAdmin(EventoLEventUserAdmin):
    resource_class = EventUserAttendanceDateResource
    list_display = ('get_user', 'get_event', 'date', 'mode',)
    list_filter = ('date', 'mode', EventFromEventUserFilter,)


class HardwareAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('model', 'type', 'manufacturer',)
    list_filter = ('type', 'manufacturer',)
    search_fields = ('model', 'type', 'manufacturer',)


class InstallationAdmin(ExportMixin, EventoLAdmin):
    resource_class = InstallationResource
    list_display = ('hardware', 'software', 'get_event', 'get_installer', 'attendee',)
    list_filter = (
        EventFromInstallerFilter, HardwareFilter, SoftwareFilter, InstallerFilter,
    )
    search_fields = ('notes',)

    def get_event(self, obj):
        return obj.installer.event
    get_event.short_description = _('Event')
    get_event.admin_order_field = 'installer__event__name'

    def get_installer(self, obj):
        return obj.installer.user
    get_installer.short_description = _('Installer')
    get_installer.admin_order_field = 'installer__user__username'

    def filter_event(self, events, queryset):
        return queryset.filter(installer__event__in=events)


class InstallationMessageAdmin(EventoLAdmin):
    list_display = ('contact_email', 'event',)
    list_filter = (EventFilter,)
    search_fields = ('contact_email', 'message',)


class InstallerAdmin(EventoLEventUserAdmin):
    resource_class = InstallerResource
    list_display = ('get_user', 'get_event', 'level',)
    list_filter = (EventFromEventUserFilter, UserFromEventUserFilter, 'level',)


class OrganizerAdmin(EventoLEventUserAdmin):
    resource_class = OrganizerResource


class ReviewerAdmin(EventoLEventUserAdmin):
    resource_class = ReviewerResource


class RoomAdmin(EventoLAdmin):
    list_display = ('name', 'event',)
    list_filter = (EventFilter,)
    search_fields = ('name', 'event__name',)


class SoftwareAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('name', 'type',)
    list_filter = ('type',)
    search_fields = ('name', 'type',)


class TicketAdmin(EventoLAdmin):
    resource_class = TicketResource
    list_display = ('get_user', 'get_event', 'sent',)
    list_filter = ('sent', UserFromEventUserSetFilter, EventFromEventUserSetFilter)
    search_fields = (
        'eventuser__user__username', 'eventuser__user__first_name',
        'eventuser__user__last_name', 'eventuser__user__email',
        'eventuser__event__name',
    )

    def get_user(self, obj):
        user = obj.eventuser_set.first()
        if user is None:
            return None
        return user.user
    get_user.short_description = _('User')
    get_user.admin_order_field = 'eventuser__user__username'

    def get_event(self, obj):
        user = obj.eventuser_set.first()
        if user is None:
            return None
        return user.event
    get_event.short_description = _('Event')
    get_event.admin_order_field = 'eventuser__event__name'
