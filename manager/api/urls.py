from django.conf.urls import patterns, url, include
from manager.api import views
from manager.api.routes import router

urlpatterns = patterns(
    '',
    url(r'^(?i)(?P<sede_url>[a-zA-Z0-9-_]+)/sede_report$', views.sede_report, name='sede report'),
    url(r'^(?i)(?P<sede_url>[a-zA-Z0-9-_]+)/sede_report2$', views.sede_report2, name='sede report2'),

    # Django REST
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
