from django.conf.urls import patterns, url, include
from manager.api import views
from manager.api.rest.router import router

urlpatterns = patterns(
    '',
    url(r'^(?i)(?P<event_url>[a-zA-Z0-9-_]+)/event_report$', views.event_report, name='event report'),
    url(r'^(?i)(?P<event_url>[a-zA-Z0-9-_]+)/event_full_report$', views.event_full_report, name='event_full_report'),

    # Django REST
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
