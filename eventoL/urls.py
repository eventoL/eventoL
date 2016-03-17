import autocomplete_light
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from eventoL import settings
from manager import views

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name="home"),
    url(r'^api/', include('manager.api.urls')),
    url(r'^create-event/$', views.create_event, name="create_event"),
    url(r'^event/', include('manager.urls'), name='event'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^grappelli/', include('grappelli.urls'), name='grappelli'),
    url(r'^ckeditor/', include('ckeditor.urls'), name='ckeditor'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^accounts/password-reset/$', auth_views.password_reset,
        {'template_name': 'accounts/password_reset/reset.html'}, name='forgot_password'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'accounts/password_reset/done.html'}, name="password_reset_done"),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'accounts/password_reset/confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password_reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'accounts/password_reset/complete.html'},
        name='password_reset_complete'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
