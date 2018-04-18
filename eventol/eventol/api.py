"""
    Api module with serializers and viewsets for models
"""
# pylint: disable=too-many-ancestors
# pylint: disable=missing-docstring

from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework_filters import FilterSet, BooleanFilter
from manager.models import (Event, Activity, Attendee, EventUserAttendanceDate,
                            Installer, Installation, Collaborator, Room,
                            EventUser, Organizer, AttendeeAttendanceDate,
                            Software, Hardware)


# Serializers define the API representation.
class EventolSerializer(QueryFieldsMixin,
                        serializers.HyperlinkedModelSerializer):
    pass


class EventSerializer(EventolSerializer):
    attendees_count = serializers.IntegerField(read_only=True)
    last_date = serializers.DateField(read_only=True)
    activity_proposal_is_open = serializers.BooleanField(read_only=True)
    registration_is_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = ('url', 'name', 'abstract', 'limit_proposal_date', 'slug',
                  'external_url', 'email', 'event_information', 'updated_at',
                  'schedule_confirmed', 'place', 'image', 'cropping', 'uid',
                  'activity_proposal_is_open', 'registration_is_open',
                  'attendees_count', 'last_date', 'created_at')


class EventUserSerializer(EventolSerializer):
    class Meta:
        model = EventUser
        fields = ('url', 'event', 'created_at')


class InstallerSerializer(EventolSerializer):
    class Meta:
        model = Installer
        fields = ('url', 'level', 'created_at')


class CollaboratorSerializer(EventolSerializer):
    class Meta:
        model = Collaborator
        fields = ('url', 'created_at')


class OrganizerSerializer(EventolSerializer):
    class Meta:
        model = Organizer
        fields = ('url', 'created_at')


class ActivitySerializer(EventolSerializer):
    class Meta:
        model = Activity
        fields = ('url', 'created_at', 'event', 'title', 'room',
                  'start_date', 'end_date', 'type', 'labels')


class AttendeeSerializer(EventolSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'created_at', 'event', 'is_installing')


class InstallationSerializer(EventolSerializer):
    class Meta:
        model = Installation
        fields = ('url', 'created_at', 'event')


class RoomSerializer(EventolSerializer):
    class Meta:
        model = Room
        fields = ('url', 'name', 'event')




# Filters
class EventFilter(FilterSet):
    activity_proposal_is_open = BooleanFilter(name='activity_proposal_is_open')
    registration_is_open = BooleanFilter(name='registration_is_open')

    class Meta:
        model = Event
        fields = ('name', 'slug', 'schedule_confirmed',
                  'activity_proposal_is_open', 'registration_is_open')


# ViewSets define the view behavior.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = EventFilter
    ordering_fields = ('name', 'limit_proposal_date', 'updated_at',
                       'attendees_count', 'last_date', 'created_at')
    search_fields = ('name', 'slug', 'abstract')

    def list(self, request):
        my_events = request.GET.get('my_events', None)
        if my_events:
            if request.user.is_authenticated():
                event_users = EventUser.objects.filter(user=request.user)
                event_ids = [event_user.event.pk for event_user in event_users]
                queryset = Event.objects.filter(pk__in=event_ids)
                slug = request.GET.get('slug', None)
                if slug:
                    queryset = Event.objects.filter(slug=slug)
            else:
                queryset = Event.objects.none()
            serializer = EventSerializer(queryset, many=True, context={'request': request})
            return Response({'results': serializer.data})
        return super().list(request)


class EventUserViewSet(viewsets.ModelViewSet):
    queryset = EventUser.objects.all()
    serializer_class = EventUserSerializer
    # filter_class = EventUserFilter
    ordering_fields = ('created_at',)
    search_fields = None


class InstallerViewSet(viewsets.ModelViewSet):
    queryset = Installer.objects.all()
    serializer_class = InstallerSerializer
    ordering_fields = ('created_at',)
    search_fields = None


class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer
    ordering_fields = ('created_at',)
    search_fields = None


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    ordering_fields = ('created_at',)
    search_fields = None


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    ordering_fields = ('created_at',)
    search_fields = ('title', 'labels',)


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    ordering_fields = ('created_at',)
    search_fields = None


class InstallationViewSet(viewsets.ModelViewSet):


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('event__uid', 'name',)
    ordering_fields = ('name',)
    search_fields = ('name',)

    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    ordering_fields = ('created_at',)
    search_fields = None
