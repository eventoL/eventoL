"""
   Routing Module with all Demultiplexers and channel_routing for djnago-channels
"""

from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class

from manager.binding import (ActivityBinding, AttendeeAttendanceDateBinding,
                             EventBinding, EventUserAttendanceDateBinding,
                             InstallationBinding)


class APIDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'activities': ActivityBinding.consumer,
        'attendeeattendancedates': AttendeeAttendanceDateBinding.consumer,
        'events': EventBinding.consumer,
        'eventuserattendancedates': EventUserAttendanceDateBinding.consumer,
        'installations': InstallationBinding.consumer,
    }

    def connection_groups(self, **kwargs):
        return ['activities-updates', 'attendeeattendancedates-updates',
                'events-updates', 'eventuserattendancedates-updates',
                'installation-updates']


channel_routing = [
    route_class(APIDemultiplexer, path='^/updates/$')
]
