from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

from manager import views
from django.conf.urls.static import static
from eventoL import settings
import autocomplete_light

autocomplete_light.autodiscover()
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name="home"),
    url(r'^api/', include('manager.api.urls')),
    url(r'^sede/', include('manager.urls'), name='sede'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^grappelli/', include('grappelli.urls'), name='grappelli'),
    url(r'^ckeditor/', include('ckeditor.urls'), name='ckeditor'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    # Hacks to preserve an old distributed url
    url(r'^proponer-charla$', RedirectView.as_view(url='/sede/talk/proposal/', permanent=True)),
    url(r'^page/informacion-del-festival$', RedirectView.as_view(url='/event', permanent=True)),
    url(r'^registracion$', RedirectView.as_view(url='/sede/registration', permanent=True)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
