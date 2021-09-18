from django.contrib.admin.options import TabularInline

from manager.models import CustomField, Event, EventDate


class EventDateAdminInline(TabularInline):
    model = EventDate


class EventTagInline(TabularInline):
    model = Event.tags.through


class FieldAdminInline(TabularInline):
    model = CustomField
    exclude = ('visible', 'placeholder_text',)
