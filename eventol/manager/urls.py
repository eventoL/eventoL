from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from manager import views
from manager.forms import (SoftwareAutocomplete, AttendeeAutocomplete,
                           EventUserAutocomplete)

event_patterns = [
    url(r'^$', views.index, name="index"),
    url(r'^attendee/confirm/(?P<pk>\d+)/(?P<token>\w+)$',
        views.attendee_confirm_email, name='attendee_confirm_email'),
    url(r'^FAQ$', views.event_view, name="FAQ", kwargs={'html': 'FAQ.html'}),
    url(r'^edit$', views.edit_event, name='edit_event'),
    url(r'^draw', views.draw, name='draw'),
    url(r'^registration$', views.attendee_registration,
        name='attendee_registration'),
    url(r'^registration/attendee/email-sent$',
        TemplateView.as_view(
            template_name='registration/attendee/email-sent.html'),
        name='attendee_email_sent'),
    url(r'^registration/attendee/search/(?P<pk>\d+)$',
        views.attendance_by_ticket, name='attendance_by_ticket'),
    url(r'^registration/attendee/search', views.manage_attendance,
        name='manage_attendance'),
    url(r'^registration/attendee/by-collaborator$',
        views.attendee_registration_by_collaborator,
        name='attendee_registration_by_collaborator'),
    url(r'^registration/collaborator$', views.collaborator_registration,
        name='collaborator_registration'),
    url(r'^registration/installer$', views.installer_registration,
        name='installer_registration'),
    url(r'^installation$', views.installation, name='installation'),
    url(r'^activity/(?P<activity_id>\d+)/$', views.activity_detail,
        name='activity_detail'),
    url(r'^activity/proposal/$', views.activity_proposal,
        name='activity_proposal'),
    url(r'^activity/proposal/image-cropping/(?P<activity_id>\d+)/$',
        views.image_cropping, name='image_cropping'),
    url(r'^activity/proposal/image-cropping/$', views.image_cropping,
        name='image_cropping'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^reports$', views.reports, name='reports'),
    url(r'^organizers$', views.add_organizer, name='add_organizer'),
    url(r'^registration_people', views.add_registration_people,
        name='add_registration_people'),
    url(r'^ticket$', views.view_ticket, name='view_ticket'),
]

urlpatterns = [
    url(r'^(?i)(?P<event_slug>[a-zA-Z0-9-_]+)/', include(event_patterns)),
    url(r'^software-autocomplete', SoftwareAutocomplete.as_view(),
        name='software-autocomplete'),
    url(r'^attendee-autocomplete', AttendeeAutocomplete.as_view(),
        name='attendee-autocomplete'),
    url(r'^eventuser-autocomplete', EventUserAutocomplete.as_view(),
        name='eventuser-autocomplete')
]
