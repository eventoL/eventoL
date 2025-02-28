from django.contrib.admin.options import TabularInline

from manager.models import Event, EventDate


class EventDateAdminInline(TabularInline):
    model = EventDate


class EventTagInline(TabularInline):
    model = Event.tags.through
