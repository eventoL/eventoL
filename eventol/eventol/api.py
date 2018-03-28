"""
    Api module with serializers and viewsets for models
"""
# pylint: disable=too-many-ancestors
# pylint: disable=missing-docstring

from django.contrib.auth.models import User
from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers, viewsets
from rest_framework_filters import FilterSet, BooleanFilter
from manager.models import Event


# Serializers define the API representation.
class EventSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer):
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
