from django.conf.urls import patterns, url, include
from manager.api import views

urlpatterns = patterns(
    '',
    url(r'^(?i)(?P<sede_url>[a-zA-Z0-9-_]+)/schedule/talks', views.talks, name='scheduled_talks'),
    url(r'^states$', views.states, name='states'),
    url(r'^cities$', views.cities, name='cities'),
    url(r'^sedes$', views.sedes, name='sedes'),
    url(r'^sedes_geo$', views.sedes_geo, name='sedes_geo'),
)