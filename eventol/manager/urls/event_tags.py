from django.conf.urls import url

from manager import views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)$', views.event_tag_index, name='slug_index'),
]
