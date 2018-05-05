"""
    Api module with serializers and viewsets for models
"""
# pylint: disable=too-many-ancestors
# pylint: disable=missing-docstring

from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework_filters import BooleanFilter, FilterSet

from manager.models import (Activity, Attendee, Collaborator, Event, EventUser,
                            Hardware, Installation, Installer, Organizer, Room,
                            Software)


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
                  'external_url', 'report', 'event_information', 'updated_at',
                  'schedule_confirmed', 'place', 'image', 'cropping', 'uid',
                  'activity_proposal_is_open', 'registration_is_open', 'id',
                  'attendees_count', 'last_date', 'created_at', 'location')


class EventUserSerializer(EventolSerializer):
    class Meta:
        model = EventUser
        fields = ('url', 'event', 'created_at', 'updated_at')


class InstallerSerializer(EventolSerializer):
    class Meta:
        model = Installer
        fields = ('url', 'level', 'created_at', 'updated_at')


class CollaboratorSerializer(EventolSerializer):
    class Meta:
        model = Collaborator
        fields = ('url', 'created_at', 'updated_at')


class OrganizerSerializer(EventolSerializer):
    class Meta:
        model = Organizer
        fields = ('url', 'created_at', 'updated_at')


class ActivitySerializer(EventolSerializer):
    class Meta:
        model = Activity
        fields = ('url', 'created_at', 'updated_at', 'event', 'title', 'room',
                  'start_date', 'end_date', 'type', 'labels', 'level', 'status',
                  'is_dummy', 'long_description', 'abstract')


class AttendeeSerializer(EventolSerializer):
    class Meta:
        model = Attendee
        fields = ('url', 'created_at', 'updated_at', 'event', 'event_user',
                  'is_installing', 'email_confirmed', 'registration_date')


class InstallationSerializer(EventolSerializer):
    class Meta:
        model = Installation
        fields = ('url', 'created_at', 'updated_at', 'installer',
                  'hardware', 'software', 'attendee', 'notes')


class RoomSerializer(EventolSerializer):
    class Meta:
        model = Room
        fields = ('url', 'name', 'event')


class HardwareSerializer(EventolSerializer):
    class Meta:
        model = Hardware
        fields = ('type', 'model', 'manufacturer',)


class SoftwareSerializer(EventolSerializer):
    class Meta:
        model = Software
        fields = ('type', 'name',)


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

    def list(self, request, *args, **kwargs):
        my_events = request.GET.get('my_events', None)
        slug = request.GET.get('slug', None)
        if my_events:
            queryset = Event.objects.get_event_by_user(request.user, slug)
            serializer = EventSerializer(queryset, many=True, context={'request': request})
            return Response({'results': serializer.data})
        return super().list(request, *args, **kwargs)


class EventUserModelViewSet(viewsets.ModelViewSet):
    filter_fields = ('event_user__event__uid',)
    ordering_fields = ('created_at', 'updated_at')
    search_fields = None

    def get_counts(self):
        model = self.serializer_class.Meta.model
        queryset = self.filter_queryset(self.get_queryset())
        event_users = model.objects.get_event_users(queryset)
        return model.objects.get_counts(event_users)

    def list(self, request, *args, **kwargs):
        count = request.GET.get('count', None)
        if count:
            return Response(self.get_counts())
        return super().list(request, *args, **kwargs)


class EventUserViewSet(EventUserModelViewSet):
    queryset = EventUser.objects.all()
    serializer_class = EventUserSerializer
    filter_fields = ('event__uid',)


class InstallerViewSet(EventUserModelViewSet):
    queryset = Installer.objects.all()
    serializer_class = InstallerSerializer


class CollaboratorViewSet(EventUserModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer


class OrganizerViewSet(EventUserModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer


class AttendeeViewSet(EventUserModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    filter_fields = ('event_user__event__uid', 'is_installing',
                     'email_confirmed', 'event__uid')
    ordering_fields = ('created_at', 'updated_at', 'registration_date')

    def get_counts(self):
        queryset = self.filter_queryset(self.get_queryset())
        return Attendee.objects.get_counts(queryset)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('event__uid', 'name',)
    ordering_fields = ('name',)
    search_fields = ('name',)


class ActivityViewSet(EventUserModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    search_fields = ('title', 'labels', 'additional_info',
                     'speakers_names', 'long_description')
    filter_fields = ('event__uid', 'room', 'title', 'type',
                     'status', 'level', 'is_dummy')
    ordering_fields = ('created_at', 'updated_at', 'start_date', 'end_date')

    def get_counts(self):
        queryset = self.filter_queryset(self.get_queryset())
        return Activity.objects.get_counts(queryset)


class SoftwareViewSet(viewsets.ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    filter_fields = ('type', 'name',)
    search_fields = ('type', 'name',)
    ordering_fields = None


class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    filter_fields = ('type', 'model', 'manufacturer',)
    search_fields = ('type', 'model', 'manufacturer',)
    ordering_fields = None


class InstallationViewSet(EventUserModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    search_fields = ('notes')
    filter_fields = ('attendee__event__uid', 'attendee__event_user__event__uid',
                     'software', 'hardware', 'attendee')
    ordering_fields = ('created_at', 'updated_at',)

    def get_counts(self):
        queryset = self.filter_queryset(self.get_queryset())
        return Installation.objects.get_counts(queryset)
