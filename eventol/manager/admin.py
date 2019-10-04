# pylint: disable=no-init
# pylint: disable=too-few-public-methods

from django.contrib import admin
from django.contrib.auth.models import User
from forms_builder.forms.models import FormEntry, FieldEntry
from image_cropping import ImageCroppingMixin
from import_export import resources
from import_export.admin import ExportMixin

from manager.models import (Activity, ActivityType, Attendee, EventolSetting,
                            AttendeeAttendanceDate, Collaborator, Contact,
                            ContactMessage, ContactType, Event, EventDate,
                            EventTag, EventUser, EventUserAttendanceDate,
                            Hardware, Installation, InstallationMessage,
                            Installer, Organizer, Room, Software, Ticket,
                            CustomForm, CustomField,)
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
        events = [organizer.event_user.event for organizer in list(organizers)]
        if events:
            return self.filter_event(events, queryset)
        return queryset.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super() \
                .formfield_for_foreignkey(db_field, request, **kwargs)
        organizers = Organizer.objects.filter(event_user__user=request.user)
        events = [organizer.event_user.event for organizer in list(organizers)]
        queryset = None
        if db_field.name == 'room':
            queryset = Room.objects.filter(event__in=events).distinct()
        if db_field.name == 'event':
            events_pks = [event.pk for event in events]
            queryset = Event.objects.filter(pk__in=events_pks).distinct()
        if db_field.name in ['event_user', 'owner']:
            queryset = EventUser.objects.filter(event__in=events).distinct()
        if db_field.name == 'attendee':
            queryset = Attendee.objects.filter(event__in=events).distinct()
        if db_field.name == 'installer':
            queryset = Installer.objects \
                .filter(event_user__event__in=events).distinct()
        if db_field.name == 'activity_type':
            queryset = ActivityType.objects.all().distinct()
        if db_field.name == 'user':
            queryset = User.objects.none()
        if db_field.name in ['hardware', 'software', 'type', 'ticket']:
            queryset = db_field.model.objects.all().distinct()
        kwargs['queryset'] = queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EventoLEventUserAdmin(ExportMixin, EventoLAdmin):
    def filter_event(self, events, queryset):
        return queryset.filter(event_user__event__in=events)


class OrganizerResource(resources.ModelResource):
    class Meta:
        model = Organizer
        fields = ('event_user__user__first_name',
                  'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__user__date_joined')
        export_order = fields


class OrganizerAdmin(EventoLEventUserAdmin):
    resource_class = OrganizerResource


class EventUserResource(resources.ModelResource):
    class Meta:
        model = EventUser
        fields = ('user__first_name', 'user__last_name', 'user__username',
                  'user__email', 'user__date_joined')
        export_order = fields


class EventUserAdmin(ExportMixin, EventoLAdmin):
    resource_class = EventUserResource


class EventDateAdminInline(admin.TabularInline):
    model = EventDate


class EventTagInline(admin.TabularInline):
    model = Event.tags.through


class EventAdmin(EventoLAdmin):
    inlines = [EventDateAdminInline, EventTagInline]
    exclude = ['tags']

    def filter_event(self, events, queryset):
        return queryset.filter(pk__in=[event.pk for event in events])


class InstallerResource(resources.ModelResource):
    class Meta:
        model = Installer
        fields = ('event_user__user__first_name',
                  'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'level',
                  'event_user__user__date_joined')
        export_order = fields


class InstallerAdmin(EventoLEventUserAdmin):
    resource_class = InstallerResource


class InstallationResource(resources.ModelResource):
    class Meta:
        model = Installation
        fields = ('hardware__type', 'hardware__manufacturer',
                  'hardware__model', 'software__type', 'software__name',
                  'attendee__email', 'installer__user__username', 'notes')
        export_order = fields


class InstallationAdmin(ExportMixin, EventoLAdmin):
    resource_class = InstallationResource

    def filter_event(self, events, queryset):
        return queryset.filter(installer__event__in=events)


class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
        fields = ('sent',)
        export_order = fields


class TicketAdmin(EventoLAdmin):
    resource_class = TicketResource


class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = ('first_name', 'last_name', 'nickname', 'email',
                  'email_confirmed', 'is_installing',
                  'additional_info', 'registration_date')
        export_order = fields


class AttendeeAdmin(ExportMixin, EventoLAdmin):
    resource_class = AttendeeResource


class ActivityResource(resources.ModelResource):
    class Meta:
        model = Activity


class ActivityAdmin(ImageCroppingMixin, ExportMixin, EventoLAdmin):
    resource_class = ActivityResource


class CollaboratorResource(resources.ModelResource):
    class Meta:
        model = Collaborator
        fields = ('event_user__user__first_name',
                  'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__user__date_joined',
                  'phone', 'address', 'assignation', 'time_availability',
                  'additional_info')
        export_order = fields


class CollaboratorAdmin(EventoLEventUserAdmin):
    resource_class = CollaboratorResource


class FieldAdmin(admin.TabularInline):
    model = CustomField
    exclude = ('visible', 'placeholder_text',)


class FormAdmin(admin.ModelAdmin):
    formentry_model = FormEntry
    fieldentry_model = FieldEntry

    inlines = (FieldAdmin,)
    list_display = ("title", "status",)
    list_display_links = ("title",)
    list_editable = ("status",)
    list_filter = ("status",)
    search_fields = ("title",)
    radio_fields = {"status": admin.HORIZONTAL}
    fields = ('title',)


admin.site.register(CustomForm, FormAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
admin.site.register(Hardware)
admin.site.register(Software)
admin.site.register(Installer, InstallerAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(InstallationMessage, EventoLAdmin)
admin.site.register(Room, EventoLAdmin)
admin.site.register(ContactType)
admin.site.register(Contact, EventoLAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ContactMessage, EventoLAdmin)
admin.site.register(EventUser, EventUserAdmin)
admin.site.register(AttendeeAttendanceDate, EventoLAdmin)
admin.site.register(EventUserAttendanceDate, EventoLEventUserAdmin)
admin.site.register(EventTag)
admin.site.register(EventolSetting)
admin.site.register(ActivityType)
