from django.conf.urls import url

from manager import views

urlpatterns = [
    url(r'^(?P<tag>[\w-]+)$', views.event_tag_index, name='tag_index'),
]
