# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from dwitter.main.views import *

urlpatterns = patterns('',
    url(r'^home/$', home, name='home'),
    url(r'^dwit/$', dwit, name='dwit'),
    url(r'^getdwit/(?P<dwit>\d+)/$', getdwit, name='getdwit'),
    url(r'^getreplyto/(?P<dwit>\d+)/$', getreplyto, name='geterplyto'),
    url(r'^gettags/$', gettags, name='gettags'),
    url(r'^getflow/(?P<nfd>\d+)/$', getflow, name='getflow'),
    url(r'^search/$', search, name='search'),
    url(r'^haystack/',include('haystack.urls')),
    url(r'^profile/(?P<username>\w+)/$', profile, name='profile'),
    url(r'^follow/(?P<username>\w+)/$', follow, name='follow'),
    url(r'^unfollow/(?P<username>\w+)/$', unfollow, name='unfollow'),
)


