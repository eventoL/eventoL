from channels.binding.websockets import WebsocketBinding

from .models import Activity
from .models import AttendeeAttendanceDate
from .models import Event
from .models import EventUserAttendanceDate
from .models import Installation


class ActivityBinding(WebsocketBinding):
    model = Activity
    stream = "activities"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["activities-updates"]

    def has_permission(self, user, action, pk):
        return True


class AttendeeAttendanceDateBinding(WebsocketBinding):
    model = AttendeeAttendanceDate
    stream = "attendeeattendancedates"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["attendeeattendancedates-updates"]

    def has_permission(self, user, action, pk):
        return True


class EventBinding(WebsocketBinding):
    model = Event
    stream = "events"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["events-updates"]

    def has_permission(self, user, action, pk):
        return True


class EventUserAttendanceDateBinding(WebsocketBinding):
    model = EventUserAttendanceDate
    stream = "eventuserattendancedates"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["eventuserattendancedates-updates"]

    def has_permission(self, user, action, pk):
        return True


class InstallationBinding(WebsocketBinding):
    model = Installation
    stream = "installations"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["installations-updates"]

    def has_permission(self, user, action, pk):
        return True
