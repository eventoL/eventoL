from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

# from manager.forms import ActivityAdminForm
from manager.models import Organizer, Event, Attendee, Collaborator, Hardware, \
    Software, Installer, Installation, Room, ContactType, Contact, Activity, \
    ContactMessage, EventUser, Image, Speaker, InstallationMessage, Ticket
from manager.security import create_reporters_group


class EventoLAdmin(admin.ModelAdmin):
    def filter_event(self, event, queryset):
        return queryset.filter(event=event)

    def queryset(self, request):
        self.get_queryset(request)

    def get_queryset(self, request):
        queryset = super(EventoLAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        reporters = create_reporters_group()
        if request.user.groups.filter(name=reporters.name).exists():
            return queryset
        organizer = Organizer.objects.filter(event_user__user=request.user).first()
        if organizer:
            return self.filter_event(organizer.event_user.event, queryset)
        return queryset.none()


class EventoLEventUserAdmin(ExportMixin, EventoLAdmin):
    def filter_event(self, event, queryset):
        return queryset.filter(event_user__event=event)


class OrganizerResource(resources.ModelResource):
    class Meta(object):
        model = Organizer
        fields = ('event_user__user__first_name', 'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__attended', 'event_user__user__date_joined')
        export_order = fields


class OrganizerAdmin(EventoLEventUserAdmin):
    resource_class = OrganizerResource


class SpeakerResource(resources.ModelResource):
    class Meta(object):
        model = Speaker
        fields = ('event_user__user__first_name', 'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__attended', 'event_user__user__date_joined')
        export_order = fields


class SpeakerAdmin(EventoLEventUserAdmin):
    resource_class = SpeakerResource


class EventUserResource(resources.ModelResource):
    class Meta(object):
        model = EventUser
        fields = (
            'user__first_name', 'user__last_name', 'user__username', 'user__email', 'attended', 'user__date_joined')
        export_order = fields


class EventUserAdmin(ExportMixin, EventoLAdmin):
    resource_class = EventUserResource


class EventAdmin(EventoLAdmin):
    def filter_event(self, event, queryset):
        return queryset.filter(name=event.name)


class InstallerResource(resources.ModelResource):
    class Meta(object):
        model = Installer
        fields = ('event_user__user__first_name', 'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__attended', 'level', 'event_user__user__date_joined')
        export_order = fields


class InstallerAdmin(EventoLEventUserAdmin):
    resource_class = InstallerResource


class InstallationResource(resources.ModelResource):
    class Meta(object):
        model = Installation
        fields = ('hardware__type', 'hardware__manufacturer', 'hardware__model', 'software__type', 'software__name',
                  'attendee__email', 'installer__user__username', 'notes')
        export_order = fields


class InstallationAdmin(ExportMixin, EventoLAdmin):
    resource_class = InstallationResource

    def filter_event(self, event, queryset):
        return queryset.filter(installer__event=event)


class TicketResource(resources.ModelResource):
    class Meta(object):
        model = Ticket
        fields = ('sent',)
        export_order = fields


class TicketAdmin(EventoLAdmin):
    resource_class = TicketResource


class AttendeeResource(resources.ModelResource):
    class Meta(object):
        model = Attendee
        fields = ('first_name', 'last_name', 'nickname', 'email', 'email_confirmed', 'is_installing',
                  'attended', 'additional_info', 'registration_date', 'attendance_date')
        export_order = fields


class AttendeeAdmin(ExportMixin, EventoLAdmin):
    resource_class = AttendeeResource


# class ActivityAdmin(EventoLAdmin):
#    form = ActivityAdminForm


class CollaboratorResource(resources.ModelResource):
    class Meta(object):
        model = Collaborator
        fields = ('event_user__user__first_name', 'event_user__user__last_name', 'event_user__user__username',
                  'event_user__user__email', 'event_user__user__date_joined', 'phone', 'address',
                  'event_user__attended',
                  'assignation', 'time_availability', 'additional_info')
        export_order = fields


class CollaboratorAdmin(EventoLEventUserAdmin):
    resource_class = CollaboratorResource


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
admin.site.register(Activity)
admin.site.register(ContactMessage, EventoLAdmin)
admin.site.register(EventUser, EventUserAdmin)
admin.site.register(Image)
admin.site.register(Speaker, SpeakerAdmin)
