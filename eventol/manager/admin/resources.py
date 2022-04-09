# pylint: disable=no-init
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

from import_export.resources import ModelResource

from manager.models import (
    Activity, Attendee, Collaborator, EventUser, EventUserAttendanceDate, Installation,
    Installer, Organizer, Reviewer, Ticket
)


class ActivityResource(ModelResource):
    class Meta:
        model = Activity


class AttendeeResource(ModelResource):
    class Meta:
        model = Attendee
        fields = (
            'first_name', 'last_name', 'nickname', 'email', 'email_confirmed',
            'is_installing', 'additional_info', 'registration_date',
        )
        export_order = fields


class CollaboratorResource(ModelResource):
    class Meta:
        model = Collaborator
        fields = (
            'event_user__user__first_name', 'event_user__user__last_name',
            'event_user__user__username', 'event_user__user__email',
            'event_user__user__date_joined', 'phone', 'address', 'assignation',
            'time_availability', 'additional_info',
            )
        export_order = fields


class EventUserAttendanceDateResource(ModelResource):
    class Meta:
        model = EventUserAttendanceDate
        fields = (
            'date', 'mode', 'event_user__user__first_name', 'event_user__user__last_name',
            'event_user__user__username', 'event_user__user__email',
            'event_user__user__date_joined',
        )
        export_order = fields


class EventUserResource(ModelResource):
    class Meta:
        model = EventUser
        fields = (
            'user__first_name', 'user__last_name', 'user__username',
            'user__email', 'user__date_joined',
        )
        export_order = fields


class InstallationResource(ModelResource):
    class Meta:
        model = Installation
        fields = (
            'hardware__type', 'hardware__manufacturer', 'hardware__model', 'software__type',
            'software__name', 'attendee__email', 'installer__user__username', 'notes',
        )
        export_order = fields


class InstallerResource(ModelResource):
    class Meta:
        model = Installer
        fields = (
            'event_user__user__first_name', 'event_user__user__last_name',
            'event_user__user__username', 'event_user__user__email', 'level',
            'event_user__user__date_joined',
        )
        export_order = fields


class OrganizerResource(ModelResource):
    class Meta:
        model = Organizer
        fields = (
            'event_user__user__first_name', 'event_user__user__last_name',
            'event_user__user__username', 'event_user__user__email',
            'event_user__user__date_joined',
        )
        export_order = fields


class ReviewerResource(ModelResource):
    class Meta:
        model = Reviewer
        fields = (
            'event_user__user__first_name', 'event_user__user__last_name',
            'event_user__user__username', 'event_user__user__email',
            'event_user__user__date_joined',
        )
        export_order = fields


class TicketResource(ModelResource):
    class Meta:
        model = Ticket
        fields = ('sent',)
        export_order = fields
