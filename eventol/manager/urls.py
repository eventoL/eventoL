from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from manager import views
from manager.forms import (SoftwareAutocomplete, AttendeeAutocomplete,
                           EventUserAutocomplete, AllAttendeeAutocomplete)

event_patterns = [
    url(r'^$', views.index, name="index"),
    url(r'^attendee/confirm/(?P<attendee_id>\d+)/(?P<token>\w+)$',
        views.attendee_confirm_email, name='attendee_confirm_email'),
    url(r'^FAQ$', views.event_view, name="FAQ", kwargs={'html': 'FAQ.html'}),
    url(r'^edit$', views.edit_event, name='edit_event'),
    url(r'^image-cropping/$', views.event_add_image, name='event_add_image'),
    url(r'^draw', views.draw, name='draw'),
    url(r'^rooms/list/$', views.rooms_list, name='rooms_list'),
    url(r'^rooms/add/$', views.add_or_edit_room, name='add_room'),
    url(r'^rooms/edit/(?P<room_id>\d+)/$', views.add_or_edit_room, name='edit_room'),
    url(r'^rooms/delete/(?P<room_id>\d+)/$', views.delete_room, name='delete_room'),
    url(r'^registration$', views.attendee_registration,
        name='attendee_registration'),
    url(r'^registration/attendee/email-sent$',
        TemplateView.as_view(
            template_name='registration/attendee/email-sent.html'),
        name='attendee_email_sent'),
    url(r'^registration/attendee/search/(?P<ticket_code>\w+)$',
        views.attendance_by_ticket, name='attendance_by_ticket'),
    url(r'^registration/attendee/search', views.manage_attendance,
        name='manage_attendance'),
    url(r'^registration/attendee/by-collaborator$',
        views.registration_by_collaborator,
        name='attendee_registration_by_collaborator'),
    url(r'^registration/attendee/from-installation$',
        views.registration_from_installation,
        name='attendee_registration_from_installation'),
    url(r'^registration/attendee/by-self/(?P<event_registration_code>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-'
        r'[89aAbB][a-f0-9]{3}-[a-f0-9]{12})$',
        views.attendee_registration_by_self,
        name='attendee_registration_by_self'),
    url(r'^registration/attendee/by-self/autoreadqr', views.attendance_by_autoreadqr,
        name='attendance_by_autoreadqr'),
    url(r'^registration/print-code$',
        views.attendee_registration_print_code,
        name='attendee_registration_print_code'),
    url(r'^registration/collaborator$', views.collaborator_registration,
        name='collaborator_registration'),
    url(r'^registration/installer$', views.installer_registration,
        name='installer_registration'),
    url(r'^installation$', views.installation, name='installation'),
    url(r'^activities$', views.activities, name='activities'),
    url(r'^activity/(?P<activity_id>\d+)/$', views.activity_detail,
        name='activity_detail'),
    url(r'^activity/proposal/$', views.activity_proposal,
        name='activity_proposal'),
    url(r'^activity/proposal/image-cropping/(?P<activity_id>\d+)/$',
        views.image_cropping, name='image_cropping'),
    url(r'^activity/proposal/image-cropping/$', views.image_cropping,
        name='image_cropping'),
    url(r'^activity/registration/(?P<proposal_id>\d+)$', views.talk_registration, name='talk_registration'),
    url(r'^activity/confirm_schedule/$', views.confirm_schedule, name='confirm_schedule'),
    url(r'^activity/reject_activity/(?P<activity_id>\d+)/$', views.reject_activity, name='reject_activity'),
    url(r'^activity/resend_proposal/(?P<activity_id>\d+)/$', views.resend_proposal, name='resend_proposal'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^reports$', views.reports, name='reports'),
    url(r'^organizers$', views.add_organizer, name='add_organizer'),
    url(r'^registration_people', views.add_registration_people,
        name='add_registration_people'),
    url(r'^ticket$', views.view_ticket, name='view_ticket'),
]

event_uid_patterns = [
    url(
        r'^(?P<event_uid>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/',
        include(event_patterns)
    ),
    url(r'^$', views.event_slug_index, name='slug_index'),
]

urlpatterns = [
    url(r'^(?i)(?P<event_slug>[a-zA-Z0-9-_]+)/', include(event_uid_patterns)),
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
