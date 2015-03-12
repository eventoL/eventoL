from django.conf.urls import patterns, url, include
from manager.api import views

urlpatterns = patterns('',
                       url(r'^states$', views.states, name='states'),
                       url(r'^cities$', views.cities, name='cities'),
                       url(r'^sedes$', views.sedes, name='sedes'),
                       url(r'^sedes_geo$', views.sedes_geo, name='sedes_geo'),
)