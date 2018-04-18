from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.views.i18n import JavaScriptCatalog
from eventol import settings
from manager import views
from rest_framework import routers

from .api import (EventViewSet, EventUserViewSet, InstallerViewSet,
                  CollaboratorViewSet, OrganizerViewSet, ActivityViewSet,
                  AttendeeViewSet, InstallationViewSet, RoomViewSet,
                  SoftwareViewSet, HardwareViewSet)


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'eventUsers', EventUserViewSet)
router.register(r'installers', InstallerViewSet)
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'organizers', OrganizerViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'attendees', AttendeeViewSet)
router.register(r'softwares', SoftwareViewSet)
router.register(r'installations', InstallationViewSet)

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^api/', include(router.urls)),
    url(r'^create-event/$', views.create_event, name="create_event"),
    url(r'^event/', include('manager.urls'), name='event'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls'), name='ckeditor'),
    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='account/profile.html'),
        name="user_profile"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(),
        {'domain': 'djangojs', 'packages': None}, name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
