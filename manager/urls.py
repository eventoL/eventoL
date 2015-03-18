from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from manager import views
from manager.views import TalkDetailView


sede_patterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^event$', views.event, name="event_info"),
    url(r'^FAQ$', views.sede_view, name="FAQ", kwargs={'html': 'FAQ.html'}),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^registration/confirm$', views.sede_view, name="confirm_registration",
        kwargs={'html': 'registration/confirm.html'}),
    url(r'^registration/success$', views.sede_view, name="success_registration",
        kwargs={'html': 'registration/success.html'}),
    url(r'^registration/collaborator$', views.collaborator_registration, name='collaborator_registration'),
    url(r'^registration/installer$', views.installer_registration, name='installer_registration'),
    url(r'^registration/become_installer$', views.become_installer, name='become_installer'),
    url(r'^registration/attendee/search$', views.attendee_search, name='attendee_search'),
    url(r'^registration/attendee/assisted$', views.sede_view,
        name="attendee_assisted", kwargs={'html': 'registration/attendee/assisted.html'}),
    url(r'^registration/attendee/by-collaborator$', views.attendee_registration_by_collaborator,
        name='attendee_registration_by_collaborator'),
    url(r'^installation$', views.installation, name='installation'),
    url(r'^installation/success$', views.sede_view, kwargs={'html': 'installation/success.html'},
        name='installation_success'),
    url(r'^talk/proposal/image-cropping/(?P<image_id>\d+)/$', views.image_cropping, name='image_cropping'),
    url(r'^talk/proposal/image-cropping/$', views.image_cropping, name='image_cropping'),
    url(r'^talk/proposal/$', views.talk_proposal, name='talk_proposal'),
    url(r'^talk/confirm$', views.sede_view, kwargs={'html': 'talks/confirm.html'}, name='talk_confirm'),
    url(r'^talk/detail/(?P<pk>\d+)$', TalkDetailView.as_view(), name='talk_detail'),
    url(r'^schedule$', views.talks, name='talks'),
    url(r'^contact$', views.contact)
)

urlpatterns = patterns(
    '',
    url(r'^(?P<sede_url>[a-zA-Z0-9-_]+)/', include(sede_patterns)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)