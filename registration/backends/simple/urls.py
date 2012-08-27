from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from registration.views import activate
from registration.views import register


urlpatterns = patterns('',
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.simple.SimpleBackend'},
                           name='registration_register'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
                       )
