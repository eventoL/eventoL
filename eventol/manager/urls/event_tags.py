from django.urls import re_path

from manager import views

urlpatterns = [
    re_path(r'^(?P<tag>[\w-]+)$', views.event_tag_index, name='tag_index'),
]
