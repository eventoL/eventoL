# pylint: disable=no-self-use

from django.contrib import admin
from django.utils.translation import gettext as _
from import_export.admin import ExportMixin

from manager.admin.filters import EventFromEventUserFilter
from manager.admin.utils import filter_model_queryset_by_user
from manager.models import Organizer
from manager.security import create_reporters_group


class EventoLAdmin(admin.ModelAdmin):
    @staticmethod
    def filter_event(events, queryset):
        return queryset.filter(event__in=events)

    def queryset(self, request):
        self.get_queryset(request)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        reporters = create_reporters_group()
        if request.user.groups.filter(name=reporters.name).exists():
            return queryset

        organizers = Organizer.objects.filter(event_user__user=request.user)
        events = [organizer.event_user.event for organizer in organizers.iterator()]
        if events:
            return self.filter_event(events, queryset)
        return queryset.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        kwargs['queryset'] = filter_model_queryset_by_user(
            request.user, db_field.remote_field.model
        )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EventoLEventUserAdmin(ExportMixin, EventoLAdmin):
    list_display = ('get_user', 'get_event',)
    list_filter = (EventFromEventUserFilter,)
    search_fields = (
        'event_user__event__name', 'event_user__user__username',
        'event_user__user__first_name', 'event_user__user__last_name',
        'event_user__user__email',
    )

    def get_user(self, obj):
        return obj.event_user.user
    get_user.short_description = _('User')
    get_user.admin_order_field = 'event_user__user__username'

    def get_event(self, obj):
        return obj.event_user.event
    get_event.short_description = _('Event')
    get_event.admin_order_field = 'event_user__event__name'

    def filter_event(self, events, queryset):
        return queryset.filter(event_user__event__in=events)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'has_background', 'has_logo_header', 'has_logo_landing',)

    def has_background(self, obj):
        return bool(obj.background is not None and obj.background)
    has_background.boolean = True
    has_background.short_description = _('Has background')

    def has_logo_header(self, obj):
        return bool(obj.logo_header is not None and obj.logo_header)
    has_logo_header.boolean = True
    has_logo_header.short_description = _('Has logo header')

    def has_logo_landing(self, obj):
        return bool(obj.logo_landing is not None and obj.logo_landing)
    has_logo_landing.boolean = True
    has_logo_landing.short_description = _('Has logo landing')
