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
    url(r'^$', views.home, name="index"),
    url(r'^app/', include('manager.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event$', TemplateView.as_view(template_name='event/info.html'), name="event_info"),
    url(r'^confirm/', include('generic_confirmation.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^FAQ$', TemplateView.as_view(template_name='FAQ.html'), name="FAQ"),

    # Hacks to preserve an old distributed url
    url(r'^proponer-charla$', RedirectView.as_view(url='/app/talk/proposal/', permanent=True)),
    url(r'^page/informacion-del-festival$', RedirectView.as_view(url='/event', permanent=True)),
    url(r'^registracion$', RedirectView.as_view(url='/app/registration', permanent=True)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
