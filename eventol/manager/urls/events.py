from django.conf.urls import url, include
from django.views.generic import RedirectView

from manager.forms import (SoftwareAutocomplete, AttendeeAutocomplete,
                           EventUserAutocomplete, AllAttendeeAutocomplete)
from .event import event_patterns

urlpatterns = [
    url(r'^(?P<event_slug>[\w-]+)/', include(event_patterns), name='event'),
    url(r'^software-autocomplete', SoftwareAutocomplete.as_view(),
        name='software-autocomplete'),
    url(r'^attendee-autocomplete', AttendeeAutocomplete.as_view(),
        name='attendee-autocomplete'),
    url(r'^all-attendee-autocomplete', AllAttendeeAutocomplete.as_view(),
        name='all-attendee-autocomplete'),
    url(r'^eventuser-autocomplete', EventUserAutocomplete.as_view(),
        name='eventuser-autocomplete'),
    url(r'^$', RedirectView.as_view(pattern_name='home')),
]
