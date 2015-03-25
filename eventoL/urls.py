from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from manager import views
from django.conf.urls.static import static
from django.contrib.auth import views as django_views
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
    url(r'^confirm/', include('generic_confirmation.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/password-reset/$', django_views.password_reset,
        {'template_name': 'registration/password_reset/reset.html'}, name='forgot_password'),
    url(r'^accounts/password_reset/done/$', django_views.password_reset_done,
        {'template_name': 'registration/password_reset/done.html'}, name="password_reset_done"),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django_views.password_reset_confirm,
        {'template_name': 'registration/password_reset/confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password_reset/complete/$', django_views.password_reset_complete,
        {'template_name': 'registration/password_reset/complete.html'},
        name='password_reset_complete'),

    # Hacks to preserve an old distributed url
    url(r'^proponer-charla$', RedirectView.as_view(url='/sede/talk/proposal/', permanent=True)),
    url(r'^page/informacion-del-festival$', RedirectView.as_view(url='/event', permanent=True)),
    url(r'^registracion$', RedirectView.as_view(url='/sede/registration', permanent=True)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
