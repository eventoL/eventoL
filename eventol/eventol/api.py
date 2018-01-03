"""
    Api module with serializers and viewsets for models
"""
# pylint: disable=too-many-ancestors
# pylint: disable=missing-docstring

from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers, viewsets
from manager.models import Event


# Serializers define the API representation.
class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('url', 'name', 'abstract', 'limit_proposal_date', 'slug',
                  'external_url', 'email', 'event_information',
                  'schedule_confirmed', 'place', 'image', 'cropping',
                  'activity_proposal_is_open', 'registration_is_open',
                  'attendees_count', 'last_date')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.annotate(attendees_count=Count('attendee'))
    serializer_class = EventSerializer
    ordering_fields = ('name', 'limit_proposal_date',
                       'attendees_count', 'last_date')
    search_fields = ('name', 'slug', 'abstract')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
