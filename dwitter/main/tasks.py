# -*- coding: utf-8 -*- 

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from celery import task
from dwitter.main.utils import emit_to_channel
from dwitter.main.models import DPF, Dwit
import json
import re
import subprocess

@task
def celery_dwitsaved(dwit, rendered):
    if dwit.direct:
        fers = dwit.member.followers.filter(user__username=re.match('^\@\w+',dwit.content).group(0)[1:])
    else:
        fers = dwit.member.followers.all()
    for fer in fers:
        DPF.objects.create(member = fer, dwit = dwit, stamp = dwit.stamp)
        emit_to_channel(fer.user.username, 'newdwit', json.dumps({'content':rendered}))
    tags = dwit.tags.all()
    if tags:
        for tag in tags:
            emit_to_channel(tag.name, 'newdwit', json.dumps({'content':rendered}))

@task
def celery_follow(me, m):
    dwits = Dwit.objects.filter(member=m)
    for dwit in dwits:
        DPF.objects.create(member = me, dwit = dwit, stamp = dwit.stamp)

@task
def celery_unfollow(me, m):
    DPF.objects.filter(member = me, dwit__member=m).delete()

@task
def celery_send_mail(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, [to_email])

@task
def haystack():
    p1 = subprocess.Popen([settings.PYTHON_ENV,settings.PROJECT_MANAGE,'update_index'],stdout=subprocess.PIPE)
    p1.communicate()


