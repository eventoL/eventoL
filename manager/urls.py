from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from manager import views
from manager.views import TalkDetailView

urlpatterns = patterns('',
    url(r'^api/', include('manager.api.urls')),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^registration/confirm$', TemplateView.as_view(template_name='registration/confirm.html'), name="confirm_registration"),
    url(r'^registration/success$', TemplateView.as_view(template_name='registration/success.html'), name="success_registration"),
    url(r'^registration/collaborator$', views.collaborator_registration, name='collaborator_registration'),
    url(r'^registration/installer$', views.installer_registration, name='installer_registration'),
    url(r'^registration/attendant/search$', views.attendant_search, name='attendant_search'),
    url(r'^registration/attendant/assisted$', TemplateView.as_view(template_name='registration/attendant/assisted.html'), name="attendant_assisted"),
    url(r'^registration/attendant/by-collaborator$', views.attendant_registration_by_collaborator, name='attendant_registration_by_collaborator'),    
    url(r'^installation$', views.installation, name='installation'),
    url(r'^installation/success$', TemplateView.as_view(template_name='installation/success.html'), name='installation_success'),
    url(r'^talk/proposal/image-cropping/(?P<image_id>\d+)/$', views.image_cropping, name='image_cropping'),
    url(r'^talk/proposal/image-cropping/$', views.image_cropping, name='image_cropping'),
    url(r'^talk/proposal/$', views.talk_proposal, name='talk_proposal'),
    url(r'^talk/confirm$', TemplateView.as_view(template_name='talks/confirm.html'), name='talk_confirm'),
    url(r'^talk/detail/(?P<pk>\d+)$', TalkDetailView.as_view(), name='talk_detail'),
    url(r'^schedule$', views.talks, name='talks'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)