from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from dwitter.views import *
import socketio.sdjango

admin.autodiscover()

js_info_dict = {'packages':('dwitter.main',)}

urlpatterns = patterns('',
    url(r'^socket\.io', include(socketio.sdjango.urls)),
    url(r'^$', HomePage.as_view(), name='homepage'),
    url(r'^main/',include('dwitter.main.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.MEDIA_ROOT}),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages':('dwitter',)}),
)

