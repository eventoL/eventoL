from autocomplete_light import shortcuts as autocomplete_light
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from eventoL import settings
from manager import views

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^create-event/$', views.create_event, name="create_event"),
    url(r'^event/', include('manager.urls'), name='event'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls'), name='ckeditor'),
    url(r'^accounts/profile/', TemplateView.as_view(template_name='account/profile.html'), name="user_profile"),
    url(r'^accounts/', include('allauth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]