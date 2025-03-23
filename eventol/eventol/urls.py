from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import re_path
from django.views.generic.base import TemplateView
from django.views.i18n import JavaScriptCatalog
from manager import views
from rest_framework import routers

from eventol import settings

from .api import ActivityTypeViewSet
from .api import ActivityViewSet
from .api import AttendeeViewSet
from .api import CollaboratorViewSet
from .api import EventTagSet
from .api import EventUserViewSet
from .api import EventViewSet
from .api import HardwareViewSet
from .api import InstallationViewSet
from .api import InstallerViewSet
from .api import OrganizerViewSet
from .api import RoomViewSet
from .api import SoftwareViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"tags", EventTagSet)
router.register(r"eventUsers", EventUserViewSet)
router.register(r"installers", InstallerViewSet)
router.register(r"collaborators", CollaboratorViewSet)
router.register(r"organizers", OrganizerViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"activities", ActivityViewSet)
router.register(r"activityTypes", ActivityTypeViewSet)
router.register(r"attendees", AttendeeViewSet)
router.register(r"softwares", SoftwareViewSet)
router.register(r"hardwares", HardwareViewSet)
router.register(r"installations", InstallationViewSet)

admin.autodiscover()

urlpatterns = [
    re_path(r"^$", views.home, name="home"),
    re_path(r"^api/", include(router.urls)),
    re_path(r"^instance_details$", views.instance_details, name="instance_details"),
    re_path(r"^report$", views.generic_report, name="generic_report"),
    re_path(r"^create-event/$", views.create_event, name="create_event"),
    re_path(r"^events/", include("manager.urls.events"), name="events"),
    re_path(r"^tags/", include("manager.urls.event_tags"), name="event_tags"),
    re_path(r"^admin/", admin.site.urls, name="admin"),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls"), name="ckeditor"),
    re_path(
        r"^accounts/profile/",
        TemplateView.as_view(template_name="account/profile.html"),
        name="user_profile",
    ),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^captcha/", include("captcha.urls")),
    re_path(
        r"^jsi18n/$",
        JavaScriptCatalog.as_view(),
        {"domain": "djangojs", "packages": None},
        name="javascript-catalog",
    ),
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r"^__debug__/", include(debug_toolbar.urls))]
