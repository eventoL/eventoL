from django.conf.urls import patterns, url, include
from manager import views

sede_patterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^event$', views.event, name="event_info"),
    url(r'^FAQ$', views.sede_view, name="FAQ", kwargs={'html': 'FAQ.html'}),
    url(r'^accounts/login/$', views.login, name='eventol_login'),
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
    url(r'^talk/detail/talk/(?P<pk>\d+)$', views.talk_detail, name='talk_detail'),
    url(r'^talk/detail/proposal/(?P<pk>\d+)$', views.proposal_detail, name='proposal_detail'),
    url(r'^talk/detail/proposal/(?P<pk>\d+)/vote/(?P<vote>\d+)$', views.vote_proposal, name='vote_proposal'),
    url(r'^talk/detail/proposal/(?P<pk>\d+)/cancel_vote/$', views.cancel_vote, name='cancel_vote'),
    url(r"^talk/detail/proposal/(?P<pk>\d+)/add_comment/$", views.add_comment),
    url(r"^talk/detail/proposal/(?P<pk>\d+)/delete_comment/$", views.delete_comment),
    url(r"^talk/detail/proposal/(?P<pk>\d+)/delete_comment/(?P<comment_pk>\d+)$", views.delete_comment),
    url(r'^talk/registration/(?P<pk>\d+)$', views.talk_registration, name='talk_registration'),
    url(r'^schedule$', views.talks, name='talks'),
    url(r'^contact$', views.contact)
)

urlpatterns = patterns(
    '',
    url(r'^(?P<sede_url>[a-zA-Z0-9-_]+)/', include(sede_patterns)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)