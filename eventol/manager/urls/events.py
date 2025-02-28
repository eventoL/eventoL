from django.urls import re_path, include
from django.views.generic import RedirectView

from manager.forms import (SoftwareAutocomplete, AttendeeAutocomplete,
                           EventUserAutocomplete, AllAttendeeAutocomplete)
from .event import event_patterns

urlpatterns = [
    re_path(r'^(?P<event_slug>[\w-]+)/', include(event_patterns), name='event'),
    re_path(r'^software-autocomplete', SoftwareAutocomplete.as_view(),
        name='software-autocomplete'),
    re_path(r'^attendee-autocomplete', AttendeeAutocomplete.as_view(),
        name='attendee-autocomplete'),
    re_path(r'^all-attendee-autocomplete', AllAttendeeAutocomplete.as_view(),
        name='all-attendee-autocomplete'),
    re_path(r'^eventuser-autocomplete', EventUserAutocomplete.as_view(),
        name='eventuser-autocomplete'),
    re_path(r'^$', RedirectView.as_view(pattern_name='home')),
]
